#!/usr/bin/env python3
"""把 scenery 表裡失效的景點圖片換成臺北旅遊網新版 open API 的圖片。

背景：
    scenery.file 裡的網址來自舊版 open data（models/handle_json/taipei-attractions.json），
    路徑形如 https://www.travel.taipei/d_upload_ttn/sceneadmin/...，
    臺北旅遊網改版後全數 404（會被導向 /404.html，Content-Type 變成 text/html）。
    新版 open API 的圖片是 https://www.travel.taipei/image/{id}，可以直接 hotlink。

用法：
    # 0.（選用）先把 API 資料存成快照，這樣 server 端不必連外網
    python3 scripts/refresh_images.py fetch --out attractions.json

    # 1. 產生對照表（只讀，不動 DB）
    python3 scripts/refresh_images.py plan --out mapping.json --verify

    # 2. 人工檢查 / 修正 mapping.json 裡 status 不是 ready 的項目

    # 3. 套用（先 dry-run 看要改什麼）
    python3 scripts/refresh_images.py apply --mapping mapping.json --dry-run
    python3 scripts/refresh_images.py apply --mapping mapping.json

    # 4. 出事的話回滾
    python3 scripts/refresh_images.py rollback --backup backup_scenery_file.json

注意：
    orders / journey / booking 都有 FK 指到 scenery(id)，所以這支只做
    UPDATE scenery SET file=... WHERE id=...，絕不新增或刪除 scenery 的列。
"""

import argparse
import difflib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime

API_URL = "https://www.travel.taipei/open-api/zh-tw/Attractions/All"

# travel.taipei 在 Cloudflare 後面，會擋掉沒有瀏覽器特徵的請求（curl 會拿到 403）。
# urllib 帶上這組 header 實測可以正常取得 200。
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
}

# 自動比對救不回來、但人工確認過的對照。key/value 都是原始名稱。
MANUAL_ALIASES = {
    "新北投溫泉區": "新北投溫泉商圈",
    "北投圖書館": "臺北市立圖書館北投分館",
    "光點臺北": "SPOT光點台北電影館",
    "臺北忠烈祠": "國民革命忠烈祠",
    "自來水博物館": "臺北自來水園區",
    "基隆河左、右岸親水": "基隆河河濱自行車道",
    "冷水坑溫泉區": "陽明山國家公園_冷水坑",
    "新店溪、大漢溪與淡水河自行車道": "新店溪河濱自行車道",
    "景美溪左、右岸自行車道": "景美溪河濱自行車道",
    "內溝溪景觀生態步道": "內溝溪生態步道",
}

# 新版 open API 已經查無此景點（歇業／裁撤／整併），自動比對不該亂猜。
KNOWN_GONE = {
    "台北探索館",
    "琉園水晶博物館(暫時休館)",
    "臺北啤酒工廠(原建國啤酒廠)",
    "二格山系-指南宮貓空親山步道",
}

# 名稱正規化時要抹掉的分隔符號（新舊版命名習慣不同：- 變 _、、變 _、括號變 _）
_SEPARATORS = re.compile(r"[\s\-－—_、,，/／\\()（）\[\]【】「」]+")


# --------------------------------------------------------------------------- #
# 名稱比對
# --------------------------------------------------------------------------- #

def canonical(name):
    """把景點名稱壓成可比對的 key：全形轉半形、台/臺統一、抹掉所有分隔符號。"""
    s = unicodedata.normalize("NFKC", name or "").strip()
    s = s.replace("臺", "台")
    s = _SEPARATORS.sub("", s)
    return s.lower()


def match_one(old_name, new_by_name, new_by_canonical, all_names):
    """回傳 (matched_name or None, method, candidates)。"""
    if old_name in KNOWN_GONE:
        return None, "known_gone", []

    alias = MANUAL_ALIASES.get(old_name)
    if alias:
        if alias in new_by_name:
            return alias, "manual_alias", []
        return None, "manual_alias_stale", [alias]

    if old_name in new_by_name:
        return old_name, "exact", []

    key = canonical(old_name)
    hit = new_by_canonical.get(key)
    if hit:
        return hit, "canonical", []

    # 一方是另一方的子字串，且全表只命中一個 —— 這是最常見的改名形式
    # （士林官邸 → 士林官邸_士林官邸公園、中正紀念堂 → 國立中正紀念堂、關渡宮 → 財團法人台北市關渡宮）
    subs = [n for n in all_names if key and (key in canonical(n) or canonical(n) in key)]
    if len(subs) == 1:
        return subs[0], "substring", []
    if len(subs) > 1:
        return None, "substring_ambiguous", subs[:5]

    close = difflib.get_close_matches(key, list(new_by_canonical.keys()), n=3, cutoff=0.75)
    cands = [new_by_canonical[c] for c in close]
    if cands:
        return cands[0], "fuzzy", cands
    return None, "unmatched", difflib.get_close_matches(old_name, all_names, n=3, cutoff=0.3)


# --------------------------------------------------------------------------- #
# 資料來源
# --------------------------------------------------------------------------- #

def fetch_attractions(max_pages=40, sleep=0.3):
    """抓新版 open API 全量景點，回傳 [{id, name, images:[url]}]。"""
    out = []
    page = 1
    total = None
    while page <= max_pages:
        url = "%s?page=%d" % (API_URL, page)
        headers = dict(BROWSER_HEADERS)
        headers["Accept"] = "application/json"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            raise SystemExit("抓 open API 失敗（page=%d）：HTTP %s %s" % (page, e.code, e.reason))
        except Exception as e:
            raise SystemExit("抓 open API 失敗（page=%d）：%s: %s" % (page, type(e).__name__, e))

        total = payload.get("total", total)
        rows = payload.get("data") or []
        if not rows:
            break
        for a in rows:
            out.append({
                "id": a.get("id"),
                "name": (a.get("name") or "").strip(),
                "images": [i["src"] for i in (a.get("images") or []) if i.get("src")],
            })
        sys.stderr.write("\r抓取中… %d/%s" % (len(out), total))
        sys.stderr.flush()
        if total is not None and len(out) >= total:
            break
        page += 1
        time.sleep(sleep)
    sys.stderr.write("\n")
    return out


def load_attractions(path=None):
    """取得新版景點資料。給了 path 就讀本地快照，否則直接打 API。

    server 端不一定連得出去（Cloudflare 對機房 IP 可能更嚴），
    所以支援先在本機 fetch 存檔、把檔案帶上去再跑。
    """
    if path:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        rows = data["attractions"] if isinstance(data, dict) else data
        print("讀取景點快照 %s：%d 筆（產生於 %s）"
              % (path, len(rows),
                 data.get("fetched_at", "未知") if isinstance(data, dict) else "未知"))
        return rows
    return fetch_attractions()


def db_connect(args):
    try:
        import mysql.connector
    except ImportError:
        raise SystemExit(
            "找不到 mysql-connector-python。\n"
            "  pip install mysql-connector-python==8.4.0\n"
            "或直接在 web container 裡跑：docker compose exec web python3 scripts/refresh_images.py ..."
        )
    return mysql.connector.connect(
        host=args.db_host, port=args.db_port, user=args.db_user,
        password=args.db_password, database=args.db_name,
    )


def read_scenery(conn):
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT `id`, `stitle`, `file` FROM `scenery` ORDER BY `id`;")
    rows = cur.fetchall()
    cur.close()
    return [
        {
            "id": r["id"],
            "name": (r["stitle"] or "").strip('"').strip(),
            "file": (r["file"] or "").strip('"'),
        }
        for r in rows
    ]


def verify_image(url, timeout=15):
    """新圖回 image/*，舊的死連結會被導到 404 頁面回 text/html。"""
    headers = dict(BROWSER_HEADERS)
    headers["Accept"] = "image/avif,image/webp,image/*,*/*;q=0.8"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
            return (r.headers.get("Content-Type") or "").startswith("image/")
    except Exception:
        return False


# --------------------------------------------------------------------------- #
# plan
# --------------------------------------------------------------------------- #

def cmd_plan(args):
    conn = db_connect(args)
    try:
        scenery = read_scenery(conn)
    finally:
        conn.close()
    print("DB scenery：%d 筆" % len(scenery))

    new = load_attractions(args.attractions)
    print("新版景點資料：%d 筆" % len(new))

    new_by_name = {a["name"]: a for a in new}
    new_by_canonical = {}
    for a in new:
        new_by_canonical.setdefault(canonical(a["name"]), a["name"])
    all_names = list(new_by_name.keys())

    items = []
    for row in scenery:
        matched, method, cands = match_one(row["name"], new_by_name, new_by_canonical, all_names)
        hit = new_by_name.get(matched) if matched else None
        images = list(hit["images"]) if hit else []

        if args.verify and images:
            images = [u for u in images if verify_image(u)]

        if matched and not images:
            # 官方新 API 這筆景點就是沒附圖（例如已暫停開放的），不是比對失敗
            status = "no_images"
        elif method in ("exact", "canonical", "substring", "manual_alias"):
            status = "ready"
        elif matched:
            status = "review"          # fuzzy：比對到了但沒把握，人工看過再改成 ready
        else:
            status = "unmatched"       # 新 API 查無此景點

        items.append({
            "id": row["id"],
            "old_name": row["name"],
            "match": matched,
            "match_id": hit["id"] if hit else None,
            "method": method,
            "status": status,
            "image_count": len(images),
            "candidates": cands,
            "old_file_preview": row["file"][:120],
        })

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "api_url": API_URL,
        "verified": bool(args.verify),
        "items": items,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    ready = [i for i in items if i["status"] == "ready"]
    review = [i for i in items if i["status"] == "review"]
    no_images = [i for i in items if i["status"] == "no_images"]
    unmatched = [i for i in items if i["status"] == "unmatched"]

    print("\n對照表已寫到 %s" % args.out)
    print("  ready     %3d 筆（apply 會更新這些）" % len(ready))
    print("  review    %3d 筆（模糊比對，人工確認後把 status 改成 ready）" % len(review))
    print("  no_images %3d 筆（有對到景點，但官方新 API 這筆沒附圖）" % len(no_images))
    print("  unmatched %3d 筆（新 API 查無此景點）" % len(unmatched))
    print("  ready 以外的都會被 apply 跳過，scenery.file 維持原樣。")

    for label, group in (("review", review), ("no_images", no_images), ("unmatched", unmatched)):
        if not group:
            continue
        print("\n[%s]" % label)
        for i in group:
            print("  id=%-4s %-30s -> %-28s (%s) 候選: %s"
                  % (i["id"], i["old_name"], i["match"] or "—", i["method"],
                     "、".join(i["candidates"]) or "無"))


# --------------------------------------------------------------------------- #
# apply
# --------------------------------------------------------------------------- #

def cmd_apply(args):
    with open(args.mapping, encoding="utf-8") as f:
        plan = json.load(f)
    targets = [i for i in plan["items"] if i.get("status") == "ready" and i.get("match")]
    if not targets:
        raise SystemExit("mapping 裡沒有 status=ready 的項目，沒東西可做。")

    new = load_attractions(args.attractions)
    by_name = {a["name"]: a for a in new}
    by_id = {a["id"]: a for a in new}

    conn = db_connect(args)
    try:
        current = {r["id"]: r for r in read_scenery(conn)}

        updates = []
        for item in targets:
            sid = item["id"]
            if sid not in current:
                print("  跳過 id=%s：scenery 裡沒有這筆" % sid)
                continue

            # 以 match（景點名）為準，人工改 mapping 時通常只會改名字不會改 id。
            hit = by_name.get(item["match"])
            if hit is None and item.get("match_id") in by_id:
                hit = by_id[item["match_id"]]
                print("  注意 id=%s：找不到景點「%s」，改用 match_id=%s（%s）"
                      % (sid, item["match"], hit["id"], hit["name"]))
            if hit is None:
                print("  跳過 id=%s：新 API 查無「%s」" % (sid, item["match"]))
                continue

            images = hit["images"]
            if args.verify:
                images = [u for u in images if verify_image(u)]
            if not images:
                print("  跳過 id=%s（%s）：沒有可用圖片" % (sid, item["old_name"]))
                continue

            updates.append({
                "id": sid,
                "old_name": item["old_name"],
                "new_name": hit["name"],
                "old_file": current[sid]["file"],
                "new_file": ",".join(images),
            })

        print("\n準備更新 %d 筆：" % len(updates))
        for u in updates:
            print("  id=%-4s %-28s -> %-28s %d 張圖"
                  % (u["id"], u["old_name"], u["new_name"], len(u["new_file"].split(","))))

        if args.dry_run:
            print("\n--dry-run，沒有寫入 DB。")
            return

        with open(args.backup, "w", encoding="utf-8") as f:
            json.dump(
                {"generated_at": datetime.now().isoformat(timespec="seconds"),
                 "items": [{"id": u["id"], "file": u["old_file"]} for u in updates]},
                f, ensure_ascii=False, indent=2,
            )
        print("\n舊值已備份到 %s" % args.backup)

        cur = conn.cursor()
        cur.executemany(
            "UPDATE `scenery` SET `file`=%s WHERE `id`=%s;",
            [(u["new_file"], u["id"]) for u in updates],
        )
        conn.commit()
        print("已更新 %d 筆。" % cur.rowcount)
        cur.close()
    finally:
        conn.close()


# --------------------------------------------------------------------------- #
# rollback
# --------------------------------------------------------------------------- #

def cmd_fetch(args):
    rows = fetch_attractions()
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({
            "fetched_at": datetime.now().isoformat(timespec="seconds"),
            "source": API_URL,
            "attractions": rows,
        }, f, ensure_ascii=False, indent=2)
    print("已寫入 %s：%d 筆景點，其中 %d 筆有圖。"
          % (args.out, len(rows), sum(1 for a in rows if a["images"])))
    print("把這個檔案帶到 server，plan/apply 加 --attractions %s 就不用再連外網。" % args.out)


def cmd_rollback(args):
    with open(args.backup, encoding="utf-8") as f:
        backup = json.load(f)
    items = backup["items"]
    conn = db_connect(args)
    try:
        cur = conn.cursor()
        cur.executemany(
            "UPDATE `scenery` SET `file`=%s WHERE `id`=%s;",
            [(i["file"], i["id"]) for i in items],
        )
        conn.commit()
        print("已還原 %d 筆（備份時間 %s）。" % (cur.rowcount, backup.get("generated_at")))
        cur.close()
    finally:
        conn.close()


# --------------------------------------------------------------------------- #

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    # DB 參數掛在各子命令底下，這樣 `plan --db-host db` 這種直覺寫法才會通。
    db = argparse.ArgumentParser(add_help=False)
    db.add_argument("--db-host", default=os.getenv("MYSQL_HOST", "localhost"),
                    help="在 web container 裡跑要指定 db（compose service name）")
    db.add_argument("--db-port", type=int, default=int(os.getenv("MYSQL_PORT", "3306")))
    db.add_argument("--db-user", default=os.getenv("MYSQL_USER", "root"))
    db.add_argument("--db-password", default=os.getenv("MYSQL_PASSWORD", "0973"))
    db.add_argument("--db-name", default=os.getenv("MYSQL_DATABASE", "taipei_trip"))

    sf = sub.add_parser("fetch", help="把新版 open API 的景點資料存成本地快照")
    sf.add_argument("--out", default="attractions.json")
    sf.set_defaults(func=cmd_fetch)

    sp = sub.add_parser("plan", parents=[db], help="產生對照表，不動 DB")
    sp.add_argument("--out", default="mapping.json")
    sp.add_argument("--attractions", help="景點快照檔（省略則即時打 API）")
    sp.add_argument("--verify", action="store_true", help="逐張確認新圖真的回 image/*（慢很多）")
    sp.set_defaults(func=cmd_plan)

    sa = sub.add_parser("apply", parents=[db], help="依對照表更新 scenery.file")
    sa.add_argument("--mapping", default="mapping.json")
    sa.add_argument("--attractions", help="景點快照檔（省略則即時打 API）")
    sa.add_argument("--backup", default="backup_scenery_file.json")
    sa.add_argument("--dry-run", action="store_true")
    sa.add_argument("--verify", action="store_true")
    sa.set_defaults(func=cmd_apply)

    sr = sub.add_parser("rollback", parents=[db], help="用備份檔還原 scenery.file")
    sr.add_argument("--backup", default="backup_scenery_file.json")
    sr.set_defaults(func=cmd_rollback)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

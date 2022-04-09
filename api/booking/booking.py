from flask import Blueprint, jsonify, request
booking_bp=Blueprint("booking", __name__)

from models.pool import pool
from mysql.connector import errors

from ..user.user import get_user_status, error_massage
from datetime import date

# ==================== model ====================
def get_journey(member_id):
    try:
        # ---------- 連接資料庫 ----------
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)
        
        # ---------- 創建資料表 ----------
        sql=""" CREATE TABLE IF NOT EXISTS `journey`(
                `member_id` BIGINT,
                `scenery_id` INT,
                `date` VARCHAR(20),
                `time` VARCHAR(20),
                `price` INT,
                PRIMARY KEY(`member_id`),
                FOREIGN KEY(`member_id`) REFERENCES `member`(`id`) 
                ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY(`scenery_id`) REFERENCES `scenery`(`id`) 
                ON DELETE CASCADE ON UPDATE CASCADE
                );
            """
        cursor.execute(sql)
        print("創建資料表完成")

        # ---------- 查詢行程資料 ----------
        sql=""" SELECT `scenery_id`, `date`, `time`, `price`
                FROM `journey`
                WHERE `member_id`='%s';
            """ %(member_id)
        cursor.execute(sql)
        schedule=cursor.fetchone()
        print("查詢行程完成", id(sql))
        # print(schedule)

        # ---------- 查詢景點資料 ----------
        if (schedule != None):
            sql=""" SELECT `id`, `stitle`, `address`, `file`
                    FROM `scenery` WHERE `id`='%s';
                """ %(schedule["scenery_id"])
            cursor.execute(sql)
            record=cursor.fetchone()
            print("查詢景點完成", id(sql))
            print(record)
        
            # ---------- 處理行程資料 ----------
            data={"date": schedule["date"],
                    "time": schedule["time"],
                    "price": schedule["price"]}

            # ---------- 處理景點資料 ----------
            attraction={}
            attraction["id"]=record["id"]
            attraction["name"]=record["stitle"].strip("\"")
            attraction["address"]=record["address"].strip("\"")
            # 圖片字串處理
            images=record["file"].strip("\"")
            images=images.split(",")
            attraction["images"]=images[0]

            # ---------- 返回指定格式 ----------
            data["attraction"]=attraction
            journey={"data":data}
            print(journey)
            print("處理資料完成")
        else:
            journey=None
    except errors.Error as e:
        print(e)
    finally:
        if conn.in_transaction:
            conn.rollback()
        cursor.close()
        conn.close()
        return journey

def check_json(json):
    try:
        journey=json
        date.fromisoformat(journey["date"])
        if (journey["time"] == "morning") and (journey["price"] == 2000):
            print(journey)
        elif (journey["time"] == "afternoon") and (journey["price"] == 2500):
            print(journey)
        else:
            print("error")
            return False
    except Exception as e:
        print(e)
        return False
    else:
        print(journey["date"])
        return True

def post_journey(member_id):
    # ---------- 處理前端資料 ----------
    journey=request.get_json()
    if (check_json(journey)):
        print("ok")
        val=[]
        val.append(journey["attractionId"])
        val.append(journey["date"])
        val.append(journey["time"])
        val.append(journey["price"])
        val.append(member_id)
        val=tuple(val)
    else:
        return error_massage("輸入錯誤資訊")

    try:
        # ---------- 連接資料庫 ----------
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)

        # ---------- 創建資料表 ----------
        sql=""" CREATE TABLE IF NOT EXISTS `journey`(
                `member_id` BIGINT,
                `scenery_id` INT,
                `date` VARCHAR(20),
                `time` VARCHAR(20),
                `price` INT,
                PRIMARY KEY(`member_id`),
                FOREIGN KEY(`member_id`) REFERENCES `member`(`id`) 
                ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY(`scenery_id`) REFERENCES `scenery`(`id`) 
                ON DELETE CASCADE ON UPDATE CASCADE
                );
            """
        cursor.execute(sql)
        print("創建資料表完成")

        # ---------- 新增資料 ----------
        sql=""" INSERT INTO 
                `journey`(`scenery_id`, `date`, `time`, `price`, `member_id`)
                VALUES(%s, %s, %s, %s, %s);
            """ 
        cursor.execute(sql, val)
        conn.commit()
        print("新增資料完成", id(sql))
        return {"ok": True}
    except errors.Error as e:
        """ 新增資料失敗 && 錯誤碼: 1062...
            代表`journey` 已有相同 member_id
            primary key 重複導致無法新增
        """
        # ---------- 更改資料 ----------
        if "1062 (23000)" in str(e):
            sql=""" UPDATE `journey`
                    SET `scenery_id`=%s,
                    `date`=%s,
                    `time`=%s,
                    `price`=%s
                    WHERE `member_id`=%s;
                """
            print(val)
            cursor.execute(sql, val)
            conn.commit()
            print("更改資料完成", id(sql))
            return {"ok": True}
        else:    
            print(e)
            return error_massage("建立行程失敗"+str(e))
    finally:
        if conn.in_transaction:
            conn.rollback()
        cursor.close()
        conn.close()

def delete_journey(member_id):
    try:
        # ---------- 連接資料庫 ----------
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)

        # ---------- 刪除資料 ----------
        sql=""" DELETE FROM `journey`
                WHERE `member_id`=%s;
            """ %(member_id)
        cursor.execute(sql)
        print("刪除資料完成", id(sql))
        return {"ok": True}
    except errors.Error as e:
        print(e)
    finally:
        conn.commit()
        cursor.close()
        conn.close()

# ==================== controller ====================
@booking_bp.route("/api/booking", methods=["GET", "POST", "DELETE"])
def booking():
    user_status=get_user_status()
    if (user_status) and (request.method == "GET"):
        member_id=user_status["data"]["id"]
        return jsonify(get_journey(member_id))

    elif (user_status) and (request.method == "POST"):
        member_id=user_status["data"]["id"]
        return jsonify(post_journey(member_id))
        
    elif (user_status) and (request.method == "DELETE"):
        member_id=user_status["data"]["id"]
        return jsonify(delete_journey(member_id))

    else:
        return error_massage("尚未登入")

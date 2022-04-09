/* ==================== model ==================== */
let journey_info;
async function get_booking_api() {
    main_log("get_booking_api");
    const url="/api/booking";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "GET",
    });
    const back_json=await response.json();
    console.log(back_json);
    if (back_json == null) {
        console.log("登入中");
        journey_info=back_json
        return true
    } else if (back_json.message == "尚未登入") {
        console.log("登出中");
        return false;
    } else {
        console.log("登入中");
        journey_info=back_json;
        return true;
    }
}

function get_front_json() {
    front_json={};
    path=location.pathname;
    path=path.split("/");
    front_json["attractionId"]=parseInt(path.pop());
    const date=document.querySelector("#date");
    front_json["date"]=date.value;
    const charge=document.querySelector("#charge");
    front_json["price"]=parseInt(charge.textContent.substring(4, 8));
    if (front_json["price"] == 2000) {
        front_json["time"]="morning";
    } else if (front_json["price"] == 2500) {
        front_json["time"]="afternoon";
    }
    console.log(front_json);
    front_json=JSON.stringify(front_json);
    return front_json
}

async function post_booking_api() {
    main_log("post_booking_api");
    const url="/api/booking";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: await get_front_json(),
    });
    const back_json=await response.json();
    // console.log(back_json);
    // console.log(back_json.message);
    back_json.hasOwnProperty("ok");
    // console.log("登入中");
    if (back_json.message == "尚未登入") {
        console.log("尚未登入");
        user_box_jump();
    } else if (back_json.message == "輸入錯誤資訊") {
        console.log("輸入錯誤資訊");
    } else {
        console.log(back_json);
        jump();
    }
}

async function delete_booking_api() {
    main_log("delete_booking_api");
    const url="/api/booking";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "DELETE",
    });
    const back_json=await response.json();
    console.log(back_json);
    await window.location.reload();
}

/* ==================== view ==================== */
// 重要console.log
function main_log(output) {
    console.log("%c"+output, 
    "color: #fff; background-color: #489; "
    +"padding: 2px 5px; border-radius: 2px");
}

/* ---------- 未登入 ---------- */
//  [彈出] 登入/註冊
function user_box_jump() {
    main_log("新增:彈出介面");
    const section=document.querySelector("section");
    section.className="show";
}
//  [跳轉] 首頁
function jump_index() {
    window.location.href="/";
}


/* ---------- 已登入 ---------- */
// [跳轉] /booking
function jump() {
    window.location.href="/booking";
}

// [點擊] 刪除行程
function trash_can() {
    main_log("新增:點擊刪除");
    const check_delete=document.querySelector(".check_delete");
    check_delete.addEventListener("click", ()=>{
        console.log("ok");
        delete_booking_api();
    });
}
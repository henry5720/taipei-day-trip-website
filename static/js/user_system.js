/* ==================== model ==================== */
// 前端表單驗證
function email_validate(form_using) {
    main_log("email驗證中")
    const email=form_using["email"].value;
    let at_symbol=email.indexOf("@");   // email > @ 索引號 (沒有: -1)
    let dot_symbol=email.lastIndexOf(".");  // email > . 索引號 (沒有: -1)
    /* @在首字或沒有(<1就是0, -1)
        dot在@前面(@最小1, +2=3)
        dot在最後,倒數第2字(dot+2超過email長度)
    */
    if (at_symbol < 1 || dot_symbol < at_symbol+2 || dot_symbol+2 >= email.length){
        console.log("無效的 e-mail");
        return false;
    } else {
        console.log("有效的 e-mail");
        return true;
    }
}

function pwd_validate(form_using) {
    const pwd=form_using["pwd"].value;
    if (pwd.length==0) {
        return false;
    } else {
        return true;
    }
}

function name_validate(form_using) {
    const name=form_using["name"].value;
    console.log(name);
    if (name.length==0) {
        return false;
    } else {
        return true;
    }
}


/* ==================== view ==================== */
// 重要console.log
function main_log(output) {
    console.log("%c"+output, 
    "color: #fff; background-color: #489; "
    +"padding: 2px 5px; border-radius: 2px");
}

/* ---------- 未登入: 增加登入功能 ---------- */
// [點擊] 登入/註冊 > 彈出section(預設signin_box)
function user_box_show() {
    main_log("新增:點擊彈出");
    // 1.獲取元素
    const user_action=document.querySelector("#user_action");
    const cross=document.querySelectorAll(".cross");
    const section=document.querySelector("section");
    // 2.註冊事件
    user_action.addEventListener("click", ()=>{
        section.className="show";
    });
    cross.forEach(element => {
        element.addEventListener("click", ()=>{
            section.className="hide";
        });
    });
}

// [點擊] a(class="change_box") > 切換(登入 & 註冊) > 返回相應form
function user_box_switch() {
    main_log("新增:點擊切換");
    const signin=document.querySelector("#signin");
    const signup=document.querySelector("#signup");
    const change_box=document.querySelectorAll(".change_box");
    let count=0;
    change_box.forEach(element => {
        element.addEventListener("click", ()=>{
            if (count==0) {
                signin.className="hide";
                signup.className="user_box";
                count++;
                form_using=form_signup;
                console.log(form_using);
                input_onchange(form_using, 1);
                main_log("更改:驗證功能");
            } else {
                signup.className="hide";
                signin.className="user_box";  
                count=0;
                form_using=form_signin;
                console.log(form_using);
                input_onchange(form_using, 0);
                main_log("更改:驗證功能");
            }
        });
    });    
}

// [更改] 驗證相應form > 顯示 or 隱藏(錯誤提示)
function input_onchange(form_using, i) {
    const span=document.querySelectorAll("section > ul > li > span");
    const email=form_using["email"];
    email.addEventListener("blur", ()=>{
        if (email_validate(form_using)) {
            span[i].className="hide";
            email.style.outline="1.2px solid #489"; 
        } else {
            span[i].className="show_span";
            span[i].textContent="輸入錯誤: 信箱";
            span[i].style.color="red";
            email.style.outline="1.2px solid red";
        }
    });

    const pwd=form_using["pwd"];
    pwd.addEventListener("blur", ()=>{
        if (pwd_validate(form_using)) {
            span[i].className="hide";
            pwd.style.outline="1.2px solid #489"; 
        } else {
            span[i].className="show_span";
            span[i].textContent="尚未輸入: 密碼";
            span[i].style.color="red";
            pwd.style.outline="1.2px solid red";
        }
    });
    
    const name=form_using["name"];
    if (name != "form_signin") {
        name.addEventListener("blur", ()=>{
            if (name_validate(form_using)) {
                span[i].className="hide";
                name.style.outline="1.2px solid #489"; 
            } else {
                span[i].className="show_span";
                span[i].textContent="尚未輸入: 姓名";
                span[i].style.color="red";
                name.style.outline="1.2px solid red";
            }
        });
    }
}

// [點擊]提交(登入 or 註冊)
function click_btn() {
    const span=document.querySelectorAll("section > ul > li > span");

    const signin_btn=document.querySelector("#signin_btn");
    signin_btn.addEventListener("click", async()=>{
        const form_signin=document.forms["form_signin"];
        if (email_validate(form_signin) && pwd_validate(form_signin)) {
            console.log("PATCH");
            const email=form_signin["email"].value;
            const pwd=form_signin["pwd"].value;
            const front_json={
                                "email": email,
                                "password": pwd
                            }
            patch_user_api(JSON.stringify(front_json));
        }
        else {
            span[0].className="show_span";
            span[0].textContent="輸入內容有誤 :(";
            span[0].style.color="red";
        }
    });

    const signup_btn=document.querySelector("#signup_btn");
    signup_btn.addEventListener("click", ()=>{
        const form_signup=document.forms["form_signup"];
        if (email_validate(form_signup) && pwd_validate(form_signup) && name_validate(form_signup)) {
            console.log("POST");
            const name=form_signup["name"].value;
            const email=form_signup["email"].value;
            const pwd=form_signup["pwd"].value;
            const front_json={
                                "name": name,
                                "email": email,
                                "password": pwd
                            }
            post_user_api(JSON.stringify(front_json));
        }
        else {
            span[1].className="show_span";
            span[1].textContent="輸入內容有誤 :(";
            span[1].style.color="red";
        }
    });
}

let user_info;
// ajax > /api/user (GET, POST, PATCH, DELETE)
async function get_user_api() {
    main_log("get_user_api");
    const url="/api/user";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "GET",
    });
    const back_json=await response.json();
    const user_status=document.querySelector("#user_action > a");
    if (back_json != null) {
        console.log("登入中")
        user_status.textContent="登出系統";
        user_info=back_json;
        return true;
    } else {
        console.log("登出中")
        user_status.textContent="登入/註冊";
        return false;
    }
}
async function patch_user_api(front_json) {
    main_log("patch_user_api");
    const url="/api/user";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "PATCH",
        body: front_json,
    });
    const back_json=await response.json();
    if (back_json["ok"]) {
        window.location.reload();
    } else {
        const span=document.querySelectorAll("section > ul > li > span");
        span[0].className="show_span";
        span[0].textContent="登入失敗 QQ";
    }
}
async function post_user_api(front_json) {
    main_log("post_user_api");
    const url="/api/user";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: front_json,
    });
    const back_json=await response.json();
    const span=document.querySelectorAll("section > ul > li > span");
    if (back_json["ok"]) {
        span[1].className="show_span";
        span[1].textContent="註冊成功 :)";
    } else {
        span[1].className="show_span";
        span[1].textContent="信箱已被使用 QQ";
    }
}
async function delete_user_api() {
    main_log("delete_user_api");
    const url="/api/user";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "DELETE",
    });
    const back_json=await response.json();
    if (back_json["ok"]) {
        window.location.reload();
    }
}

/* ---------- 已登入: 增加會員功能 ---------- */
// [點擊]登出系統 > delete_user_api()
function user_sign_out() {
    main_log("新增:點擊登出");
    const user_action=document.querySelector("#user_action");
    user_action.addEventListener("click", ()=>{
        delete_user_api();
    });
}

// [點擊]預定行程 > 跳轉網頁
function click_booking() {
    main_log("新增:點擊預定");
    const booking_action=document.querySelector("#booking_action");
    booking_action.addEventListener("click", async ()=>{
        console.log("click");
        if (await get_user_api()) {
            jump();
        } else {
            user_box_jump();
        }
    });
}


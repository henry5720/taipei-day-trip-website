let back_json;
// [GET]api/order/<orderNumber>
async function api_order_get(num) {
    main_log("api/order");
    const url="/api/order/"+num;
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "GET",
    });
    back_json=await response.json();
    // console.log(back_json);


}
function handle_back_json() {
    console.log(back_json);
    const order_ul=document.querySelector(".order_result");
    console.log(order_ul.children[0]);
    li_one=order_ul.children[0];
    img=back_json["data"]["trip"]["attraction"]["image"];
    li_one.style.background="url("+img+") no-repeat center center";
    li_one.style.backgroundSize="cover";
    li_two=order_ul.children[1];
    order_info=li_two.children;
    console.log(order_info);
    order_info[0].textContent="付款完成: 單號("+back_json["data"]["number"]+")";
    order_info[1].textContent="景點: "+back_json["data"]["trip"]["attraction"]["name"];
    order_info[2].textContent="日期: "+back_json["data"]["trip"]["date"];
    order_info[3].textContent="時間: "+back_json["data"]["trip"]["time"];
}

/* ==================== controller ==================== */
window.addEventListener("load", async ()=>{
    main_log("頁面刷新:初始化");

    if (await get_user_api()) {
        user_sign_out();
    } else {
        window.location.href="/";
    }
    click_booking();
    order_num=location.search.split("=")[1]
    await api_order_get(order_num);
    handle_back_json();
    const wrapper=document.querySelector(".wrapper");
    wrapper.style.display="none";
});
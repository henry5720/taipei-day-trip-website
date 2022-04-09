/* ==================== controller ==================== */
window.addEventListener("load", async ()=>{
    main_log("頁面刷新:初始化");
    const form_signin=document.forms["form_signin"];
    const form_signup=document.forms["form_signup"];
    let form_using=form_signin;
    if (await get_user_api()) {
        user_sign_out();
    } else {
        user_box_show();
        user_box_switch();
        input_onchange(form_using, 0);
        main_log("新增:驗證功能");
        click_btn();
    }
    click_booking();

});
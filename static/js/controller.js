/* ==================== controller ==================== */
/* document.onreadystatechange=function(){
    console.log(document.readyState);
    if(document.readyState=="complete"){
        const wrapper=document.querySelector(".wrapper");
        wrapper.style.display="none";
    }
}
 */
window.addEventListener("load", async ()=>{
    main_log("load:載入完成");
    const wrapper=document.querySelector(".wrapper");
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
    wrapper.style.display="none";
});



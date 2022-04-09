/* ==================== controller ==================== */
window.addEventListener("load", async()=>{
    main_log("頁面刷新:初始化");
    await get_user_api();
    if (await get_booking_api()) {
        user_sign_out();
        click_booking();
        console.log(journey_info);
        if (journey_info != null) {
            const user_name=document.querySelector("#user_name"); 
            user_name.textContent=user_info.data.name;

            const check_img=document.querySelector(".check > img");
            check_img.src=journey_info.data.attraction.images;
            const scene_name=document.querySelector("#scene_name");
            scene_name.textContent="台北一日遊 : "+journey_info.data.attraction.name;

            const journey_info_list=document.querySelectorAll(".check-list > li > i");
            console.log(journey_info_list);
            journey_info_list.forEach(i => {
                // console.log(i);
                journey_info_list[0].textContent=journey_info.data.date;
                if (journey_info.data.time == "morning") {
                    journey_info_list[1].textContent="早上9點到下午4點"
                } else {
                    journey_info_list[1].textContent="下午4點到晚上9點"
                }
                journey_info_list[2].textContent="新台幣 "+journey_info.data.price+" 元";
                journey_info_list[3].textContent=journey_info.data.attraction.address;
            });
            const total=document.querySelector("#total");
            total.textContent="新台幣 "+journey_info.data.price+" 元";
            const main_none=document.querySelector(".main_none");
            main_none.style.display="none";
            trash_can();
        } else {
            const main=document.querySelector("main");
            main.style.display="none";

            const user_name=document.querySelector("#box__user"); 
            user_name.textContent=user_info.data.name;

        }
    } else {
        jump_index();
    }
});

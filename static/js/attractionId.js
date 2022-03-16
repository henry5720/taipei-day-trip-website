/* ====================== model ======================= */
let scenery={};
async function get_data() {
    main_log("獲取資料");
    const pathname=await location.pathname;
    const url="/api/"+pathname;
    const response=await fetch(url);
    const data=await response.json();
    scenery=data.data[0];
    return scenery
}

/* ======================= view ======================= */
function main_log(output) {
    console.log("%c"+output, 
    "color: #fff; background-color: #489; "
    +"padding: 2px 5px; border-radius: 2px");
}

function render_page() {
    /*  rendering steps
        1.[left_box]create images & control_dot
        2.[right_box]update title, category, mrt
        3.[right_box]switch charge when click
        4.[bottom_box]update description, address, transport
     */
    main_log("渲染頁面");

    // [left_box]scenery_imgs(ul), control_box(div) > ol
    const ul=document.querySelector(".scenery_imgs");
    const ol=document.querySelector(".control_box > ol");
    images=scenery.images; // all images.src

    for(let i=0; i<images.length; i++) {
        // create all li > img
        const li1=document.createElement("li");
        const img=document.createElement("img");
        ul.appendChild(li1).appendChild(img);
        // create ol > all li
        const li2=document.createElement("li");
        ol.appendChild(li2);

        // img src > scenery.images[i]
        img.setAttribute("src", images[i]);
        if (i==0) {
            img.style.opacity=1;
            li2.style.background="#000";
        }
        
    }

    // [right_box] > h2,i 
    const right_box=document.querySelector(".right_box");
    const h2=right_box.children[0];
    h2.textContent=scenery.name;
    const i=right_box.children[1];
    i.textContent=scenery.category+" at "+scenery.mrt;

    // [right_box]switch charge when click
    const morning=document.querySelector("#morning");
    const night=document.querySelector("#night");
    const charge=document.querySelector("#charge");
    morning.addEventListener("click", ()=>{
        charge.textContent="新台幣 2000元";
    });
    night.addEventListener("click", ()=>{
        charge.textContent="新台幣 2500元";
    });

    
    // [bottom_box] > li > p
    const bottom_box=document.querySelector(".bottom_box");
    const box_list=bottom_box.children;
    const p0=box_list[0].children[0];
    p0.textContent=scenery.description;
    const p1=box_list[1].children[1];
    p1.textContent=scenery.address;
    const p2=box_list[2].children[1];
    p2.textContent=scenery.transport;
}

function slideshow() {
    /* slideshow requirements
        0.initialize
        1.[click]arrow > change img
        2.span add click event
     */
    const imgs=document.querySelectorAll(".scenery_imgs > li > img");
    const spans=document.querySelectorAll(".control_box > span");
    const dots=document.querySelectorAll(".control_box > ol > li");
    let index=0;

    // 0.initialize
    function clear_active() {
        console.log("重置");
        for(let i=0; i<imgs.length; i++) {
            imgs[i].style.opacity=0;
        }
        for(let j=0; j<dots.length; j++) {
            dots[j].style.background="#fff";
        }
    }

    // 1.[click]arrow > change img
    function left_arrow(second) {
        console.log("開始"+index);
        if (index>0) {
            imgs[index].style.animation="hide_left "+second;
            index--;
            imgs[index].style.animation="show_left "+second+" forwards";
            dots[index].style.background="#000";
        } else {
            imgs[index].style.animation="hide_left "+second;
            dots[index].style.background="#fff";
            index=imgs.length-1;
            imgs[index].style.animation="show_left "+second+" forwards";
            dots[index].style.background="#000";            
        }
        main_log("結束"+index);
    }
    function right_arrow(second) {
        console.log("開始"+index);
        if (index<imgs.length-1) {
            imgs[index].style.animation="hide_right "+second;
            index++;
            imgs[index].style.animation="show_right "+second+" forwards";
            dots[index].style.background="#000";    
        } else {
            imgs[index].style.animation="hide_right "+second;
            dots[index].style.background="#fff";
            index=0;
            imgs[index].style.animation="show_right "+second+" forwards";
            dots[index].style.background="#000";            
        }
        main_log("結束"+index);
    }

    // 2.span add click event
    spans[0].addEventListener("click", ()=>{
        clear_active();
        left_arrow("1s");
    });
    spans[1].addEventListener("click", ()=>{
        clear_active();
        right_arrow("1s");
    });
}


/* ==================== controller ==================== */
window.addEventListener("load", async()=>{
    main_log("頁面加載")
    await get_data();
    await render_page();
    await slideshow();
});
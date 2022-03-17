/*  Part 2 - 2：串接景點 API，取得並展示第一頁的景點資訊
    1.fetch > api/attractions
    2.from api get data (json)
    3.create element and append imgs
*/
/* Part 2 - 3：完成自動載入後續頁面的功能
    1.record the required data (nextPage)
    2.create IntersectionObserver (.copyright) 
    3.stop calling api continuously
    4.get next page information
 */ 
/* Part 2 - 4：完成關鍵字搜尋功能
    1.record keyword
    2.fetch > api/attractions
    3.show the results 
*/

// function ==================================================
function main_log(output) {
    console.log("%c"+output, 
    "color: #fff; background-color: #489; "
    +"padding: 2px 5px; border-radius: 2px");
}

let search_imgs=async (page, keyword)=>{
    // fetch > get json
    const url="/api/attractions?page="+page+"&keyword="+keyword;
    const response=await fetch(url);
    const json=await response.json();
    data=json.data;
    // console.log(data[0].id);

    const ul=document.querySelector(".container");
    // set function(li > a > img,h3 > span,span > i,i)
    function create(box) {
        return document.createElement(box);
    }
    
    // show the query results
    if (data.length==0) {
        main_log("執行search_imags: 查無資料");
        remove_lis();
        let h1=create("h1");
        ul.appendChild(h1);
        h1.textContent="沒有 "+keyword+" 的搜尋結果";
    }else {
        main_log("執行search_imags: 存在資料");
            // for loop > append imgs and content
        for(i=0; i<data.length; i++) { // data.length=12
            // create elements
            let li=create("li");
            let a=create("a");
            let img=create("img");
            let h3=create("h3");
            let span1=create("span");
            let span2=create("span");
            let i1=create("i");
            let i2=create("i");

            // append elements
            a=ul.appendChild(li).appendChild(a);
            a.appendChild(img)
            h3=a.appendChild(h3)
            h3.appendChild(span1)
            span2=h3.appendChild(span2)
            span2.appendChild(i1)
            span2.appendChild(i2)

            // append content
            img.src=data[i].images[0];
            span1.textContent=data[i].name;
            i1.textContent=data[i].mrt;
            i2.textContent=data[i].category;

            // change a.href (/attraction/<id>)
            a.setAttribute("href", "/attraction/"+data[i].id);
        }
    }

    // record the required data (nextPage)
    const next_page=document.querySelector(".next_page")
    next_page.textContent=json.nextPage
}

let get_next=async()=>{
    const next_page=await document.querySelector(".next_page")
    const search=await document.querySelector("#search_text");
    page=await next_page.textContent;
    keyword=await search.value;

    if (page != "" && keyword == "輸入景點名稱查詢") {
        page=next_page.textContent;
        keyword="";
        await console.log("執行get_next(A): "+page, keyword);
        await search_imgs(page, keyword);
    }else if (page != "" && keyword != "輸入景點名稱查詢") {
        page=next_page.textContent;
        keyword=search.value;
        await console.log("執行get_next(B): "+page, keyword);
        await search_imgs(page, keyword);
    }else if (page == "" && keyword == "輸入景點名稱查詢") {
        page=null;
        keyword=null;
        await console.log("執行get_next(C): "+page, keyword);
    }else {
        page=null;
        keyword=search.value;
        await console.log("執行get_next(D): "+page, keyword);
    }
    return [page,keyword]
}

let lazy_load=async()=>{
    // create IntersectionObserver (.copyright)
    const footer=document.querySelector(".copyright");
    let observer = new IntersectionObserver(async(e) => {
        let isintersecting = e[0].isIntersecting;
        // console.log(e[0].intersectionRatio);
        if (isintersecting) {
            await main_log("顯示中")
            // stop calling api continuously
            let step=0;
            if (step==0) {
                get_next();
                // get next page information
                step++;
            } else {
                observer.unobserve(footer);
                step=0;
            }
        }else{
            await console.log("隱藏中");
        }
    }, {
        root: null // options
    });
    observer.observe(footer);
}

let remove_lis=()=>{
    main_log("清除完成");
    const ul=document.querySelector(".container");
    while(ul.hasChildNodes())
    { 
        ul.removeChild(ul.firstChild); 
    }
}

// execute ==================================================

window.addEventListener("load", async ()=>{
    const btn=document.querySelector("#search_btn");
    const search=document.querySelector("#search_text");

    let page=0;
    let keyword="";
    await search_imgs(page, keyword);
    await lazy_load();

    search.addEventListener("focus",()=>{
        if (search.value=="輸入景點名稱查詢"){
            search.value="";
        }
    });
    search.addEventListener("blur", ()=>{
        if (search.value==""){
            search.value="輸入景點名稱查詢";
            keyword="";
        } else {
            keyword=search.value
        }
    });

    btn.addEventListener("click", ()=>{
        remove_lis();
        search_imgs(page, keyword);
    });
});
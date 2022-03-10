/*  Part 2 - 2：串接景點 API，取得並展示第一頁的景點資訊
    1.fetch > api/attractions
    2.from api get data (json)
    3.create element and append imgs
*/

// function ==================================================
let get_imgs=async (page) => {
    let url="../api/attractions?page="+page

    // 1.fetch > api/attractions
    let response=await fetch(url);
    let json=await response.json();

    // 2.from api get data (json)
    let data=json.data
    // console.log(data);
    
    // 3.create element and append imgs
    // a.get elements(main > ul)
    const ul=document.querySelector(".container");

    // b.set function(li > a > img,h3 > span,span > i,i)
    function create(box) {
        return document.createElement(box);
    }

    // c.for loop > append imgs and content
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
    }

    // 1.record the required data (nextPage)
    const next_page=document.querySelector(".next_page")
    next_page.textContent=json.nextPage
    console.log("nextPage: "+next_page.textContent);
    
}
// 4.get next page information
let get_next=() => {
    const next_page=document.querySelector(".next_page")
    page=next_page.textContent;

    if (page != 0 && page != null) {
        get_imgs(page);
    }else {
        console.log("nextPage:"+null);
    }
    return page
}

// execute ==================================================
/* Part 2 - 3：完成自動載入後續頁面的功能
    1.record the required data (nextPage)
    2.create IntersectionObserver (.copyright) 
    3.stop calling api continuously
    4.get next page information
 */ 
window.onload=function() {
    let page=0;
    get_imgs(page);

    // 2.create IntersectionObserver (.copyright)
    const footer=document.querySelector(".copyright");
    let observer = new IntersectionObserver((e) => {
        let isintersecting = e[0].isIntersecting;
        // console.log(e[0].intersectionRatio);
        if (isintersecting) {
            console.log("target in sight");
            // 3.stop calling api continuously
            let step=0;
            if (step==0) {
                // 4.get next page information
                get_next();
                step++;
            } else {
                observer.unobserve(footer);
                step=0;
            }
        }else{
            console.log("target not in sight");
        }
    }, {
        root: null
    });
    observer.observe(footer);
}

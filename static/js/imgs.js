/*  Part 2 - 2：串接景點 API，取得並展示第一頁的景點資訊
    1.fetch to api/attractions
    2.get first picture from api
    3.create element and append imgs
*/

let get_imgs=async () => {
    const url="../api/attractions"

    let response=await fetch(url);
    let json=await response.json();
    
    data=json.data
    console.log(data);
    
    // 1.獲取元素(main > ul)
    ul=document.querySelector(".container");

    // 2.創建元素 (li > a > img,h3 > span,span > i,i)
    function create(box) {
        return document.createElement(box);
    }
    // li=create("li");
    // ul.appendChild(li);

    //3.遍歷創建元素 > 新增圖片&內容
    for(i=0; i<data.length; i++) {
        li=create("li");
        a=create("a");
        img=create("img");
        h3=create("h3");
        span1=create("span");
        span2=create("span");
        i1=create("i");
        i2=create("i");

        a=ul.appendChild(li).appendChild(a);
        a.appendChild(img)
        h3=a.appendChild(h3)
        
        h3.appendChild(span1)
        span2=h3.appendChild(span2)
        span2.appendChild(i1)
        span2.appendChild(i2)

        first_img=data[i].images[0];
        scene=data[i].name;
        mrt=data[i].mrt;
        category=data[i].category;

        img.src=data[i].images[0];
        span1.textContent=data[i].name;
        i1.textContent=data[i].mrt;
        i2.textContent=data[i].category;

    }
}
get_imgs();

/* 景點圖片載入失敗時換成佔位圖。

   scenery.file 裡有少數景點還留著臺北旅遊網改版前的舊網址（/d_upload_ttn/...），
   那些網址現在會被導向 404 頁面。這些景點（已停業、暫停開放、或整併掉的）
   在官方新版 open API 裡本來就查無圖片，沒有東西可以換，
   所以在前端擋掉破圖。

   用法：一定要在設 img.src 之前呼叫，不然 error 事件已經錯過了。
       set_img_fallback(img);
       img.src = "...";
*/

const IMG_PLACEHOLDER = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 280">' +
    '<rect width="400" height="280" fill="#E8E8E8"/>' +
    '<rect x="130" y="70" width="140" height="105" rx="8"' +
    ' fill="none" stroke="#66AABB" stroke-width="5"/>' +
    '<circle cx="240" cy="98" r="11" fill="#AADDEE"/>' +
    '<path d="M138 170 L178 124 L206 152 L228 134 L262 170 Z" fill="#66AABB"/>' +
    '<text x="200" y="215" text-anchor="middle" fill="#757575"' +
    ' font-family="sans-serif" font-size="22">暫無照片</text>' +
    '</svg>'
);

function on_img_error(e) {
    const img = e.currentTarget;
    // 換過一次就把 listener 拿掉，避免佔位圖本身出事時無限迴圈
    img.removeEventListener("error", on_img_error);
    img.src = IMG_PLACEHOLDER;
}

function set_img_fallback(img) {
    img.addEventListener("error", on_img_error);
}

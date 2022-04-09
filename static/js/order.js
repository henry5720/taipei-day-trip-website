const APP_ID = '124014';
const APP_KEY = 'app_o2V82MS6xtPR1sOD8OUDsk1FHmU7O7I2j8gTPZMNzD59cAG6sYfnmZs410os';

const submit = document.querySelector('#submit_button');
const message=document.querySelector("#message");

const status = {
    '0': '欄位已填妥',
    '1': '欄位未填妥',
    '2': '欄位有錯誤',
    '3': '輸入中',
};
const style = {
    'input': {
        'color': 'gray'
    },
    'input.ccv': {
        // 'font-size': '16px'
    },
    ':focus': {
        'color': 'black'
    },
    '.valid': {
        'color': 'green'
    },
    '.invalid': {
        'color': 'red'
    },
    '@media screen and (max-width: 400px)': {
        'input': {
            'color': 'orange'
        }
    }
}
const config = {
    isUsedCcv: true,
};

// [初始化]使用 APP_ID 和 APP_KEY 
TPDirect.setupSDK(APP_ID, APP_KEY, 'sandbox');

// [載入]信用卡表單
TPDirect.card.setup({
    fields: {
        number: {
            element: document.querySelector(".card-number"),
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            element: document.getElementById('tappay-expiration-date'),
            placeholder: 'MM / YY'
        },
        ccv: {
            element: document.querySelector(".cvc"),
            placeholder: '後三碼'
        }
    },
    styles: style
});

// [檢查]信用卡表單, [更改]依結果反饋畫面
function tap_pay_get_prime() {
    main_log("TapPay取得Prime")
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            console.log('getPrime 錯誤');
            message.textContent="輸入有錯誤";
            return;
        }
        prime = result.card.prime;
        console.log('getPrime 成功: ' + prime);
        message.textContent="";
    });
}

// [組織]json格式資訊
function handle_front_json(prime) {
    // console.log(journey_info);
    let command = {};
    command["prime"]=prime;
    command["order"]={};
    command["order"]["price"]=journey_info["data"]["price"];
    command["order"]["trip"]=journey_info["data"];
    command["order"]["contact"]={};
    const contact_name=document.querySelector("#contact_name");
    command["order"]["contact"]["name"]=contact_name.value;
    const contact_email=document.querySelector("#contact_email");
    command["order"]["contact"]["email"]=contact_email.value;
    const contact_phone=document.querySelector("#contact_phone");
    command["order"]["contact"]["phone"]=contact_phone.value;
    return command
}

// [POST]api/orders
async function api_orders_post(command) {
    main_log("api/orders");
    const url="/api/orders";
    const response=await fetch(url, {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: "POST",
        body: command,
    });
    const back_json=await response.json();
    console.log(back_json);
    try {
        pay_status=back_json["data"]["payment"]["status"]
        if (pay_status==0) {
            delete_booking_api();
            jump_thank(back_json["data"]["number"]);
        } else {
            message.textContent="付款失敗";
        }
    } catch (error) {
        console.log(error);
        message.textContent="輸入有錯誤";
    }
}

// [跳轉]/thankyou
function jump_thank(num) {
    window.location.href="/thankyou?number="+num;
}

// [增加]點擊事件(getPrime)
submit.addEventListener('click',() => {
    // 讓 button click 之後觸發 getPrime 方法
    TPDirect.card.getPrime((result) => {
        main_log("TapPay取得Prime");
        let prime=null;
        if (result.status !== 0) {
            console.log('getPrime 錯誤');
            message.textContent="輸入有錯誤";
            return;
        }
        prime=result.card.prime;
        console.log('getPrime 成功: ' + prime);
        message.textContent="";
        front_json=handle_front_json(prime);
        console.log(front_json);
        // 將 prime 送往後端 api
        api_orders_post(JSON.stringify(front_json));
    });
});
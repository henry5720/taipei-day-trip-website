from flask import Blueprint, jsonify, request
orders_bp=Blueprint("orders", __name__)

import json
import requests

from models.pool import pool
from mysql.connector import errors

from ..user.user import get_user_status, error_massage

import os
from dotenv import load_dotenv
load_dotenv()

# ==================== model ====================
""" ---------- api/orders ---------- """
# [處理]前端資料 > 資料庫所需val(tuple)
def orders_json(member_id):
    orders=request.get_json()
    scenery_id=orders["order"]["trip"]["attraction"]["id"]
    date=orders["order"]["trip"]["date"]
    time=orders["order"]["trip"]["time"]
    price=orders["order"]["price"]
    name=orders["order"]["contact"]["name"]
    email=orders["order"]["contact"]["email"]
    phone=orders["order"]["contact"]["phone"]
    if (name!="") and (email!="") and (phone!=""):
        val=(member_id, scenery_id, date, time, price, name, email, phone)
        print(val)
        return val
    else:
        return False

# [創建]資料庫訂單資料
def post_orders(val):
    try:
        # ---------- 連接資料庫 ----------
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)

        # ---------- 創建資料表 ----------
        sql=""" CREATE TABLE IF NOT EXISTS `orders`(
                `order_number` BIGINT AUTO_INCREMENT,
                `member_id` BIGINT,
                `scenery_id` INT,
                `date` VARCHAR(20),
                `time` VARCHAR(20),
                `price` INT,
                `name` VARCHAR(64),
                `email` VARCHAR(64),
                `phone` VARCHAR(20),
                `payment_status` BOOLEAN DEFAULT 0,
                PRIMARY KEY(`order_number`),
                FOREIGN KEY(`member_id`) REFERENCES `member`(`id`) 
                ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY(`scenery_id`) REFERENCES `scenery`(`id`) 
                ON DELETE CASCADE ON UPDATE CASCADE
                );
            """
        cursor.execute(sql)
        print("創建資料表完成")
        

        # ---------- 新增資料 ----------
        sql=""" INSERT INTO 
                `orders`(`member_id`, `scenery_id`, 
                            `date`, `time`, `price`,
                            `name`, `email`, `phone`)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s);
            """ 
        cursor.execute(sql, val)
        conn.commit()
        print("新增資料完成", id(sql))
        return True
    except errors.Error as e:
        print(e)
        return error_massage("服器內部錯誤"), 500
    finally:
        if conn.in_transaction:
            conn.rollback()
        cursor.close()
        conn.close()

# [查詢]資料庫目前訂單
def select_order_number(member_id):
    try:
        # ---------- 連接資料庫 ----------
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)

        # ---------- 查詢資料 ----------
        sql=""" SELECT `order_number` 
                FROM `orders` 
                WHERE `member_id`=%s;
            """ %(member_id)
        cursor.execute(sql)
        records=cursor.fetchall()
        print("查詢資料完成", id(sql))
    except errors.Error as e:
        print(e)
        return error_massage("服器內部錯誤"), 500
    finally:
        if conn.in_transaction:
            conn.rollback()
        cursor.close()
        conn.close()
        now_order=records.pop()
        print("records:", now_order)
        return now_order

# [處理]前端&資料庫資料 > TapPay所需格式
def payment_info(record):
    orders=request.get_json()
    prime=orders["prime"]
    partner=os.getenv("PARTNER")
    merchant_id=os.getenv("MERCHANT_ID")
    price=orders["order"]["price"]
    name=orders["order"]["contact"]["name"]
    email=orders["order"]["contact"]["email"]
    phone=orders["order"]["contact"]["phone"]

    payload={
                "prime": prime,
                "partner_key": partner,
                "merchant_id": merchant_id,
                "details":"TapPay Test",
                "amount": price,
                "cardholder": {
                    "phone_number": phone,
                    "name": name,
                    "email": email,
                },
                "order_number": record,
                "remember": True
            }
    print(payload)
    return json.dumps(payload)

# [付款]TapPay所需格式 > TapPay API(連接銀行)
# [返回]回傳資料裡的status(成功與否的狀態碼)
def payment_bank(payload):
    url="https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    headers={
        "x-api-key": "partner_Tri7Rb7WdWdFz2ZR1iPa2SEmzUg7KFeDeR3dn4TYX2Tl9prVjNt4Xw5h",
        "Content-Type": "application/json"
        }
    response=requests.post(url, data=payload, headers=headers)
    print(json.loads(response.text))
    return json.loads(response.text)

# [更改]根據status狀態碼 > 數據庫是否更改訂單狀態
def payment_status(member_id, order_number):
    try:
        # ---------- 連接資料庫 ----------
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)
        # ---------- 跟新資料 ----------
        sql=""" UPDATE `orders`
                SET `payment_status`=TRUE
                WHERE `member_id`=%s 
                AND `order_number`=%s;
            """ %(member_id, order_number)
        cursor.execute(sql)
        conn.commit()
        print("跟新資料完成", id(sql))
    except errors.Error as e:
        print(e)
        return error_massage("服器內部錯誤"), 500
    finally:
        if conn.in_transaction:
            conn.rollback()
        cursor.close()
        conn.close()

# [返回]訂單結果, 指定格式
def order_result(record, pay_status, message):
    order_result={
                    "data": {
                        "number": record,
                        "payment": {
                            "status": pay_status,
                            "message": message
                        }
                    }
                }
    return order_result

""" ---------- api/order/<orderNumber> ---------- """
# [查詢]資料庫訂單資料, [使用]訂單編號
def get_orders(member_id, orderNumber):
    try:
        # ---------- 連接資料庫 ----------
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)

        # ---------- 查詢訂單資料 ----------
        sql=""" SELECT * FROM `orders` 
                WHERE `member_id`=%s
                AND `order_number`=%s;
            """ %(member_id, orderNumber)
        cursor.execute(sql)
        order_record=cursor.fetchone()
        print("查詢訂單完成", id(sql))
        # ---------- 查詢景點資料 ----------
        sql=""" SELECT `stitle`, `address`, `file`
                FROM `scenery` WHERE `id`=%s;
            """ %(order_record["scenery_id"])
        cursor.execute(sql)
        scene_record=cursor.fetchone()
        return [order_record, scene_record]
    except errors.Error as e:
        print(e)
        return error_massage("服器內部錯誤"), 500
    finally:
        if conn.in_transaction:
            conn.rollback()
        cursor.close()
        conn.close()

def result_order(order_info):
    # 圖片字串處理
    images=order_info[1]["file"].strip("\"")
    images=images.split(",")
    result={
            "data": {
                "number": order_info[0]["order_number"],
                "price": order_info[0]["price"],
                "trip": {
                    "attraction": {
                        "id": order_info[0]["scenery_id"],
                        "name": order_info[1]["stitle"].strip("\""),
                        "address": order_info[1]["address"].strip("\""),
                        "image": images[0]
                    },
                    "date": order_info[0]["date"],
                    "time": order_info[0]["time"]
                },
                "contact": {
                    "name": order_info[0]["name"],
                    "email": order_info[0]["email"],
                    "phone": order_info[0]["phone"]
                },
                "status": order_info[0]["payment_status"]
            }
    }
    return result
# ==================== controller ====================
@orders_bp.route("/api/orders", methods=["POST"])
def api_orders():
    user_status=get_user_status()
    try:
        member_id=user_status["data"]["id"]
        val=orders_json(member_id)
        if (val):
            post_orders(val)
            record=select_order_number(member_id)["order_number"]
            payload=payment_info(record)
            pay_status=payment_bank(payload)["status"]
            if (pay_status == 0):
                payment_status(member_id, record)
                success=order_result(record, pay_status, "付款成功")
                return jsonify(success)
            else:
                failed=order_result(record, 1, "付款失敗")
                return jsonify(failed)
        else:
            return error_massage("輸入錯誤"), 400
    except:
        return error_massage("尚未登入"), 403

@orders_bp.route("/api/order/<orderNumber>", methods=["GET"])
def api_order(orderNumber):
    user_status=get_user_status()
    if (user_status):
        member_id=user_status["data"]["id"]
        order_info=get_orders(member_id, orderNumber)
        result=result_order(order_info)
        print(result)
        return jsonify(result)
    else:
        return error_massage("尚未登入"), 403

from flask import Blueprint, jsonify, request, make_response
user_system_bp=Blueprint("user", __name__)

from models.pool import pool
from mysql.connector import errors

import jwt
from datetime import datetime, timedelta

# ==================== model ====================
def error_massage(massage):
    return {
            "error": True,
            "message": massage
            }

class Auth:
    jwt_key="cryptic"
    inform={}

def get_user_status():
    try:
        user_inform=request.cookies.get("user_inform", None)
        payload=jwt.decode(user_inform, Auth.jwt_key, algorithms=["HS256"])
        print("解析請求token")
        if (payload != Auth.inform):
            print("token驗證失敗")
            payload=None
    except jwt.PyJWTError as e:
        print("token驗證失敗", e)
        payload=None
    finally:
        return payload

def post_user_signup():
    try:
        Auth.inform=request.get_json()
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)
        sql=""" CREATE TABLE IF NOT EXISTS `member`(
                `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
                `name` VARCHAR(64) NOT NULL,
                `email` VARCHAR(64) NOT NULL,
                `password` VARCHAR(64) NOT NULL
                );
            """
        cursor.execute(sql)
        print("創建資料表完成")
        sql=""" SELECT `id` FROM `member`
                WHERE `email` = '%s';
            """ %(Auth.inform["email"])
        cursor.execute(sql)
        record=cursor.fetchone()
        if (len(Auth.inform) == 3)and(record == None):
            record={"ok": True}
            sql=""" INSERT INTO
                    `member`(`name`, `email`, `password`) 
                    VALUES(%s, %s, %s);
                """
            val=(Auth.inform["name"], Auth.inform["email"], Auth.inform["password"])
            cursor.execute(sql, val)
            cursor.close()
            conn.commit()
            print("註冊會員成功")
        elif (len(Auth.inform) == 3)and(record != None):
            record=error_massage("email already in use")
        else:
            record=error_massage("input error")
    except Exception as e:
        print(e)
        record=error_massage("server error")
    finally:
        conn.close()
        return jsonify(record)

def patch_user_signin():
    try:
        email=request.get_json()["email"]
        password=request.get_json()["password"]
        conn=pool.get_connection()
        print("連接數據庫完成: ", conn.connection_id)
        cursor=conn.cursor(dictionary=True)
        sql=""" SELECT `id`, `name`, `email` FROM `member`
                WHERE `email` = '%s' AND `password` = '%s';
            """ %(email, password)
        cursor.execute(sql)
        records=cursor.fetchall()
        # print(records)
        if (records != []):
            print("帳密匹對成功")
            Auth.inform=dict(data=records[0])
            print("紀錄認證資訊:", Auth.inform)
            token=jwt.encode(Auth.inform, Auth.jwt_key, algorithm='HS256')
            print("生成JWT_token", token)
            response=make_response(jsonify({"ok": True}))
            response.set_cookie(key="user_inform", value=token, max_age=60*60*24*7)
            print("設置cookie成功")
            return response
        else:
            print("找不到相應帳密")
            return error_massage("input error")
    except errors.Error as e:
        print(e)
        return error_massage("server error"), 500
    finally:
        cursor.close()            
        conn.close()
        print("斷開數據庫連線")
    
# ==================== controller ====================
@user_system_bp.route("/api/user", methods=["GET", "POST", "PATCH", "DELETE"])
def user_system():
    if (request.method == "GET"):
        return jsonify(get_user_status())

    if (request.method == "POST"):
        return post_user_signup()
        
    if (request.method == "PATCH"):
        return patch_user_signin()

    if (request.method == "DELETE"):
        response=make_response(jsonify({"ok": True}))
        response.set_cookie(key="user_inform", value="", max_age=0)
        print("cookie刪除成功")
        Auth.inform={}
        return response



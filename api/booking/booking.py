from flask import Blueprint, jsonify, request, make_response
booking_bp=Blueprint("booking", __name__)

from models.pool import pool
from mysql.connector import errors

import jwt
from datetime import datetime, timedelta
from ..user.user import Auth, get_user_status



@booking_bp.route("/api/booking", methods=["GET", "POST", "DELETE"])
def booking():
    if (request.method == "GET"):
        payload=get_user_status()
        return "GET"

    if (request.method == "POST"):
        try:
            journey=request.get_json()
            print(journey)
            conn=pool.get_connection()
            print("連接數據庫完成: ", conn.connection_id)
            cursor=conn.cursor(dictionary=True)
            sql=""" CREATE TABLE IF NOT EXISTS `journey`(
                `member_id` BIGINT,
                `scenery_id` INT,
                `date` DATE,
                `time` VARCHAR(20),
                `price` INT,
                PRIMARY KEY(`member_id`, `scenery_id`),
                FOREIGN KEY(`member_id`) REFERENCES `member`(`id`) ON DELETE CASCADE,
                FOREIGN KEY(`scenery_id`) REFERENCES `scenery`(`id`) ON DELETE CASCADE
                );
            """
            cursor.execute(sql)
            print("創建資料表完成", id(sql))
            sql="""
                
                """


            cursor.close()
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            conn.close()
            return "POST"

    if (request.method == "DELETE"):
        return "DELETE"
"""Part 1 - 2：開發旅遊景點 API
"""
"""/api/attraction/{attractionId} [根據景點編號取得景點資料]
    1.取得attractionId (URL 的自訂義path)
    2.轉換attractionId格式 > 成功 (inter)
        a.sql語句 > 根據id取出資料
        b.處理資料 > json
    3.轉換attractionId格式 > 錯誤
        a.返回錯誤訊息
"""

from flask import *
search_bp=Blueprint("search", __name__)

from models.pool import pool
from mysql.connector import errors

@search_bp.route("/api/attraction/<attractionId>", methods=["GET"])
def scan_attractions(attractionId):
    # print(attractionId)
    # print(type(attractionId))
    try:
        attractionId=int(attractionId)
        # print(attractionId)
    except:
        error={
                "error": True,
                "message": "傳入錯誤參數"
            }
        return error
    

    try:
        con=pool.get_connection()
        cursor=con.cursor(dictionary=True)
        # "insert into user values(%s, %s, %s)",(1,80,"zhang")
        sql="select * from scenery where id = {}".format(attractionId)
        cursor.execute(sql)
        records=cursor.fetchone()
        # print(records)
        # print(type(records))
        dict1={}
        list1=[]
        dict2={}
        dict2["id"]=records["id"]
        dict2["name"]=records["stitle"].strip("\"")
        dict2["category"]=records["CAT2"].strip("\"")
        dict2["description"]=records["xbody"].strip("\"")
        dict2["address"]=records["address"].strip("\"")
        dict2["transport"]=records["info"].strip("\"")
        dict2["mrt"]=records["MRT"].strip("\"")
        latitude=records["latitude"].strip("\"")
        longitude=records["longitude"].strip("\"")
        images=records["file"].strip("\"")

        # 取得所需資料(轉成小數型)
        latitude=float(latitude)
        longitude=float(longitude)
        dict2["latitude"]=latitude
        dict2["longitude"]=longitude

        # 取得所需資料(圖片字串處理)
        images=images.split(",")
        dict2["images"]=images
        
        list1.append(dict2)
        dict1["data"]=list1
        # con.commit()    
    except errors.Error as e:
        print(e)
        dict3={}
        dict3["error"]=True
        dict3["massage"]="伺服器錯誤"
        return jsonify(dict3)
    finally:
        if con.in_transaction:
            con.rollback()
        con.close()
        if dict1 != {}:
            return jsonify(dict1)
        else:
            error={
                "error": True,
                "message": "傳入錯誤參數"
            }
            return error



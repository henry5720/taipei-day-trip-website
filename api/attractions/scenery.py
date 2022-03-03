"""Part 1 - 2：開發旅遊景點 API
"""
"""/api/attractions [取得景點資料列表]
    (A)取得不同分頁的旅遊景點列表資料，(B)也可以根據標題關鍵字篩選
    1.取得query string(page)
    2.sql語句 > limit x,12 (限制每頁12筆)
    3.處理資料 > json
    (B)也可以根據標題關鍵字篩選
    1.取得query string(keyword)
    2.sql語句 > WHERE?,LIKE?(篩選關鍵字)
    3.處理資料 > json
"""

from flask import *
scenery_bp=Blueprint("scenery", __name__)

from .pool import pool
from mysql.connector import errors


@scenery_bp.route("/api/attractions", methods=["GET"])
def scan_attractions():
    if (request.method=="GET"):
        """1.取得query string > 處理相應api
        """
        page=request.args.get("page", default="0")
        keyword=request.args.get("keyword", default=None)
        try:
            print(type(page))
            page=int(page)
        except:
            error={
                "massage":"input error"
            }
            return error
        if (type(page)==int)and(keyword==None)or(keyword==""):
            """連接數據庫 > 處理資料 > 回傳指定格式資料
                處理資料: (A)取得不同分頁的旅遊景點列表資料
                回傳指定格式資料: json.dumps()?, jsonify()?
            """
            print("A")
            try:
                con=pool.get_connection()
                cursor=con.cursor(dictionary=True)
                sql="SELECT * FROM `scenery` LIMIT 12 OFFSET %s;"%(page*12)             
                cursor.execute(sql)
                records=cursor.fetchall()
                # print(records)
                # print(type(records))

                dict1={}
                list1=[]
                if page < 5:
                    dict1["nextPage"]=page+1
                else:
                    dict1["nextPage"]=None

                for i in records:
                    dict2={}
                    dict2["id"]=i["id"]
                    dict2["name"]=i["stitle"]
                    dict2["category"]=i["CAT2"]
                    dict2["description"]=i["xbody"]
                    dict2["address"]=i["address"]
                    dict2["transport"]=i["info"]
                    dict2["mrt"]=i["MRT"]
                    dict2["latitude"]=i["latitude"]
                    dict2["longitude"]=i["longitude"]
                    dict2["images"]=i["file"].split()
                    list1.append(dict2)
                    dict1["data"]=list1
                    # print(json.dumps(i["stitle"]))
                    # print(i["file"].split())
                    # print(type(i["file"]))

                # print(dict1)

                con.commit()    
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
                return jsonify(dict1)
        else:
            """連接數據庫 > 處理資料 > 回傳指定格式資料
                處理資料: (B)根據標題關鍵字篩選[也需要分頁] 
            """
            print("B")
            try:
                con=pool.get_connection()
                cursor=con.cursor(dictionary=True)
                sql="select * from scenery where stitle like '%"+keyword+"%' limit 12 offset %s;"              
                # print(sql)
                cursor.execute(sql,(page*12,))
                records=cursor.fetchall()
                print(len(records))
                # print(type(records))
                

                dict1={}
                list1=[]
                if (len(records)<=12)and(len(records)!=0):
                    dict1["nextPage"]=page+1
                else:
                    dict1["nextPage"]=None

                for i in records:
                    dict2={}
                    dict2["id"]=i["id"]
                    dict2["name"]=i["stitle"]
                    dict2["category"]=i["CAT2"]
                    dict2["description"]=i["xbody"]
                    dict2["address"]=i["address"]
                    dict2["transport"]=i["info"]
                    dict2["mrt"]=i["MRT"]
                    dict2["latitude"]=i["latitude"]
                    dict2["longitude"]=i["longitude"]
                    dict2["images"]=i["file"].split()
                    list1.append(dict2)
                    dict1["data"]=list1
                    # print(json.dumps(i["stitle"]))
                    # print(i["file"].split())
                    # print(type(i["file"]))

                # print(dict1)

                con.commit()    
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
                return jsonify(dict1)

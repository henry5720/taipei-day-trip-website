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

from data.pool import pool
from mysql.connector import errors


@scenery_bp.route("/api/attractions", methods=["GET"])
def scan_attractions():
    if (request.method=="GET"):
        """1.取得query string > 處理相應api
        """
        page=request.args.get("page", default="0")
        keyword=request.args.get("keyword", default=None)
        try:
            # print(type(page))
            # query string 結果 > int(失敗: 輸入錯誤)
            page=int(page)
        except:
            error={
                "massage":"input error"
            }
            return error
        # page是int && keyword 是預設值(表示未輸入) > (A)取得不同分頁的旅遊景點列表資料
        if (type(page)==int)and(keyword==None)or(keyword==""):
            """連接數據庫 > 取得資料 > 處理資料(回傳指定格式資料)
                處理資料: (A)取得不同分頁的旅遊景點列表資料
                回傳指定格式資料: json.dumps()?, jsonify()?
            """
            try:
                print("A.取得不同分頁的旅遊景點列表資料")
                """連接數據庫"""
                # MySQLConnectionPool 建立的pool取得連線 > con
                con=pool.get_connection()

                # 預設,返回(tuple)
                # dictionary=True,返回(可迭代的cursor) / 
                cursor=con.cursor(dictionary=True)

                """取得資料"""
                # 有取到13個(表示有下一頁)
                sql="""SELECT `id`,`stitle`,`CAT2`,`xbody`,`address`,
                        `info`,`MRT`,`latitude`,`longitude`,`file`
                        FROM `scenery` LIMIT 13 OFFSET %s;
                    """%(page*12)          
                cursor.execute(sql)
                
                """處理資料(回傳指定格式資料)
                    {
                        "nextPage": 1,
                        "data": [
                            {
                                "id": 10,
                                "name": "平安鐘",
                                "category": "公共藝術",
                                "description": "平安鐘祈求大家的平安，這是為了紀念 921 地震週年的設計",
                                "address": "臺北市大安區忠孝東路 4 段 1 號",
                                "transport": "公車：204、212、212直",
                                "mrt": "忠孝復興",
                                "latitude": 25.04181,
                                "longitude": 121.544814,
                                "images": [
                                "http://140.112.3.4/images/92-0.jpg"
                                ]
                            }
                        ]
                    }
                """
                # dict & list (for flask json)
                dict1={} # dict(第1層)
                list1=[] # dict(第1層) > list(第1層)
                
                # print(type(cursor))
                # 變歷cursor > 處理資料 > dict2
                for row in cursor:   # Using the cursor as iterator
                    dict2={} # dict(第2層)

                    # 取得所需資料(去掉多餘字符)
                    dict2["id"]=row["id"]
                    dict2["name"]=row["stitle"].strip("\"")
                    dict2["category"]=row["CAT2"].strip("\"")
                    dict2["description"]=row["xbody"].strip("\"")
                    dict2["address"]=row["address"].strip("\"")
                    dict2["transport"]=row["info"].strip("\"")
                    dict2["mrt"]=row["MRT"].strip("\"")
                    latitude=row["latitude"].strip("\"")
                    longitude=row["longitude"].strip("\"")
                    images=row["file"].strip("\"")

                    # 取得所需資料(轉成小數型)
                    latitude=float(latitude)
                    longitude=float(longitude)
                    dict2["latitude"]=latitude
                    dict2["longitude"]=longitude

                    # 取得所需資料(圖片字串處理)
                    images=images.split(",") # str >list
                    dict2["images"]=images
                    # print(type(images))

                    list1.append(dict2) # 存放到 list1
                # print(list1)

                # 判斷 len(list) > 有無下一頁
                if (len(list1)==13):
                    dict1["nextPage"]=page+1
                    dict1["data"]=list1[0:-1]
                elif (len(list1)<13):
                    dict1["nextPage"]=None
                    dict1["data"]=list1
                else:
                    dict1["nextPage"]=None

                # print(len(list1))
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
                return jsonify(dict1)
        
        # keyword 有輸入 > (B)也可以根據標題關鍵字篩選
        else:
            """連接數據庫 > 處理資料 > 回傳指定格式資料
                處理資料: (B)根據標題關鍵字篩選[也需要分頁] 
            """
            try:
                print("B.也可以根據標題關鍵字篩選")
                con=pool.get_connection()
                cursor=con.cursor(dictionary=True)
                """取得資料"""
                # 有取到13個(表示有下一頁)
                sql="""SELECT `id`,`stitle`,`CAT2`,`xbody`,`address`,
                        `info`,`MRT`,`latitude`,`longitude`,`file`
                        FROM `scenery` WHERE `stitle` 
                        LIKE '%"""+keyword+"""%' LIMIT 13 OFFSET %s;
                    """
                # print(sql)
                cursor.execute(sql,(page*12,))
                
                """處理資料(回傳指定格式資料)"""
                # dict & list (for flask json)
                dict1={} # dict(第1層)
                list1=[] # dict(第1層) > list(第1層)
                
                # 變歷cursor > 處理資料 > dict2
                for row in cursor:   # Using the cursor as iterator
                    dict2={} # dict(第2層)

                    # 取得所需資料(去掉多餘字符)
                    dict2["id"]=row["id"]
                    dict2["name"]=row["stitle"].strip("\"")
                    dict2["category"]=row["CAT2"].strip("\"")
                    dict2["description"]=row["xbody"].strip("\"")
                    dict2["address"]=row["address"].strip("\"")
                    dict2["transport"]=row["info"].strip("\"")
                    dict2["mrt"]=row["MRT"].strip("\"")
                    latitude=row["latitude"].strip("\"")
                    longitude=row["longitude"].strip("\"")
                    images=row["file"].strip("\"")

                    # 取得所需資料(轉成小數型)
                    latitude=float(latitude)
                    longitude=float(longitude)
                    dict2["latitude"]=latitude
                    dict2["longitude"]=longitude

                    # 取得所需資料(圖片字串處理)
                    images=images.split(",") # str >list
                    dict2["images"]=images
                    # print(type(images))

                    list1.append(dict2) # 存放到 list1
                # print(list1)
                
                # 判斷 len(list) > 有無下一頁
                if (len(list1)==13):
                    dict1["nextPage"]=page+1
                    dict1["data"]=list1[0:-1]
                elif (len(list1)<13):
                    dict1["nextPage"]=None
                    dict1["data"]=list1
                else:
                    dict1["nextPage"]=None
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
                return jsonify(dict1)

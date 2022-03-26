""" Part 1 - 1：將景點資料存放至資料庫
    1. 抓取所有景點資料(with開啟json > mysql)
    2. 資料處理成 dict{} > sql語句 ('{data}')
    3. 存到mysql裡(json格式)
"""
import json
from pool import pool
from mysql.connector import errors

# def json_sql():
with open("taipei-attractions.json", mode="r", encoding="UTF-8") as f:
    print("打開JSON檔案成功")
    scene=json.load(f)["result"]["results"]
    # print(scene)
    # print(type(scene))
    # type(scene) > list
    list1=[]
    for i in scene: # type(i) > dict
        list2=[]
        # type(i["file"]) > str
        images=i["file"].split("https://")  # type(images) > list
        images=[i for i in images if (".jpg" in i)or(".JPG" in i)]  # type(images) > list
        images="https://"+",https://".join(images)  # type(images) > str
        images=images.split(",")    # type(images) > list
        i["file"]=images    # type(i["file"]) > list
        # print(images)
        # print(type(i["file"]))
        list2.append(i)  # type(images) > list
        list1.append(list2)
    print(list1)
        
    print("圖片篩選完成")



    try:
        con=pool.get_connection()
        print("連接數據庫完成: ", con.connection_id)
        cursor=con.cursor(dictionary=True)
        # print(scene)
        sql="""CREATE TABLE IF NOT EXISTS `scenery`(
                `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
                `data` JSON
                );
            """
        cursor.execute(sql)
        print("創建資料表完成")

        # print(eval(scene))
        for i in list1:
            i=json.dumps(i, ensure_ascii=False)
            # i=eval(i)
            print(i)
            # print(type(i))
            sql="INSERT INTO `scenery` VALUES(data, {})".format("\""+i+"\"")
            cursor.execute(sql)

        print("資料匯入成功")


        # sql=""
        con.commit()
    except errors.Error as e:
        print(e)
        # dict3={}
        # dict3["error"]=True
        # dict3["massage"]="伺服器錯誤"
    finally:
        if con.in_transaction:
            con.rollback()
        con.close()


""" Part 1 - 1：將景點資料存放至資料庫
    1. 抓取所有景點資料(with開啟json > mysql)
    2. 
    3. 存到mysql裡(json, csv, pandas?, numpy?, ...)
"""
import json
import csv
import mysql.connector
from mysql.connector import errors

def get_csv():
    with open("taipei-attractions.json", mode="r", encoding="UTF-8") as f:
        print("打開JSON檔案成功")
        scene=json.load(f)["result"]["results"]
        # print(scene)
        # print(type(scene))
        # type(scene) > list
        list1=[]
        csv_data=[]
        # print(scene.keys())
        for i in scene: # type(i) > dict
            # type(i["file"]) > str
            images=i["file"].split("https://")  # type(images) > list
            images=[i for i in images if (".jpg" in i)or(".JPG" in i)]  # type(images) > list
            images="https://"+",https://".join(images)  # type(images) > str
            # images=images.split(",")    # type(images) > list
            i["file"]=images    # type(i["file"]) > list
            csv_head=[]
            csv_head=list(i.keys())
            lv=list(i.values())
            csv_data.append(lv)
        return csv_head,csv_data,scene

get_csv()
print("資料處理完成")
# print(get_csv()[1])

"""[b]資料存到csv (delimiter: 使用特殊符號 > mysql比較好處理)
    # quoting: 碰到特殊符號(,、。；)不會導致換單元格...等操作
    # delimiter: 只有csv_data[]的分割符有換單元格的效果
"""
with open("D:/MySQL Server 8.0/Uploads/data.csv", mode="w", encoding="UTF-8-SIG", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(get_csv()[0]) # 寫入head_csv[]

    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL,delimiter='○')
    writer.writerows(get_csv()[1]) # 寫入csv_data[]
    print("資料匯入完成")

"""3. 存到mysql裡 > [a]head_csv製作初始sql(創建表格)
"""
def table_sql():
    tables=[]
    fields=[]
    for i in get_csv()[0]:
        fields.append(i)
        char=i+" TEXT"
        tables.append(char)
    tables_sql = ','.join(tables)
    # print(tables)
    sql="CREATE TABLE IF NOT EXISTS `scenery`"+"("+tables_sql+");"
    return sql,fields
# print(table_sql()[0])

"""3. 存到mysql裡 > [b]連線mysql > 執行sql語句
    (1)sql_mode問題: strict_trans_tables
        1262 (01000): Row 24 was truncated; 
        it contained more data than there were input columns
    (2)創建表格 > table_sql()
    (3)新增資料 > LOAD DATA INFILE (讀取data.csv)
        1290 (HY000): The MySQL server is running with the 
        --secure-file-priv option so it cannot execute this statement
        問題: 限制mysqld只能在/tmp目錄中執行匯入匯出,其他目錄不能執行。
    (4)新增ID列 > alter(sql)
    
    (5)修改表頭數據類型 / optional
"""
try:
    conn=mysql.connector.connect(option_files="my.conf")
    cnx=conn.cursor()
    print(conn.connection_id)
    sql="set sql_mode='no_engine_substitution';"
    cnx.execute(sql)
    print("修改模式")
    sql=table_sql()[0]
    cnx.execute(sql)
    print("創建表格")
    sql="""LOAD DATA INFILE 'D:/MySQL Server 8.0/Uploads/data.csv'
        INTO TABLE scenery
        CHARACTER SET UTF8
        FIELDS TERMINATED BY '○'
        LINES TERMINATED BY '\r\n'
        IGNORE 1 ROWS;
        """
    cnx.execute(sql)
    print("新增資料")
    sql="alter table scenery add column id int not null AUTO_INCREMENT primary key first;"
    cnx.execute(sql)
    print("新增ID")

except errors.Error as e:
    print(e)
finally:
    conn.commit()
    cnx.close()
    conn.close()




    # try:
    #     con=pool.get_connection()
    #     print("連接數據庫完成: ", con.connection_id)
    #     cursor=con.cursor(dictionary=True)
    #     # print(scene)
    #     sql="""CREATE TABLE IF NOT EXISTS `scenery`(
    #             `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
    #             `data` JSON
    #             );
    #         """
    #     cursor.execute(sql)
    #     print("創建資料表完成")

    #     # print(eval(scene))
    #     for i in list1:
    #         i=json.dumps(i, ensure_ascii=False)
    #         # i=eval(i)
    #         print(i)
    #         # print(type(i))
    #         sql="INSERT INTO `scenery` VALUES(data, {})".format("\""+i+"\"")
    #         cursor.execute(sql)

    #     print("資料匯入成功")


    #     # sql=""
    #     con.commit()
    # except errors.Error as e:
    #     print(e)
    #     # dict3={}
    #     # dict3["error"]=True
    #     # dict3["massage"]="伺服器錯誤"
    # finally:
    #     if con.in_transaction:
    #         con.rollback()
    #     con.close()


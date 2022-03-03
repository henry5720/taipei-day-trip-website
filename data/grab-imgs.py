""" Part 1 - 1：將景點資料存放至資料庫
    1. 抓取所有景點資料(with開啟資料 > json法方讀取)
    2. [a]處理資料(for loop) > [b]資料存到csv
    3. 存到mysql裡(json, csv, pandas?, numpy?, ...)
"""
import json
import csv
import mysql.connector
from mysql.connector import errors

"""1. 抓取所有景點資料(with開啟資料 > json法方讀取)
"""
with open("taipei-attractions.json", mode="r", encoding="UTF-8") as file:
    data_json=json.load(file)
    # print(data)

# 景點資訊(全部)
scene=data_json["result"]["results"]

"""2. [a]處理資料(for loop)
    head_csv: 自己需要的數據名(csv.column第一行)
    csv_data: 根據head_cs(從json裡拿到的數據)
    結果:
    head_csv = ["stitle", "CAT2",..., "file"]
    csv_data=[[],[],...,[]]
"""
def img_list():
    img_list=[] # [[],[]...]
    for i in range(1):
        imgs=(scene[i]["file"].split("https://"))
        r=[s for s in imgs if ".jpg" in s or ".JPG" in s]
        img="https://"+",https://".join(r)
        img_list.append(img)
        print(img)
    return img_list

def get_data():
    # 表頭, 所需數據名
    head_csv = ["stitle", "CAT2", "xbody", "address", "info", "MRT", "latitude", "longitude", "file"]
    csv_data = [] # 存數據的列表

# 循環遍歷json(value),增加到csv_data
    for i in range(len(scene)):
        # 存單項數據的列表,循環記錄一次後,再設為空列表[]
        # print(i)
        one_csv_data = []
        # one_csv_data.append(i["_id"])
        one_csv_data.append(scene[i]["stitle"])
        one_csv_data.append(scene[i]["CAT2"])
        one_csv_data.append(scene[i]["xbody"])
        one_csv_data.append(scene[i]["address"])
        one_csv_data.append(scene[i]["info"])
        one_csv_data.append(scene[i]["MRT"])
        one_csv_data.append(scene[i]["latitude"])
        one_csv_data.append(scene[i]["longitude"])
        # print(len(i["file"]))

        # img_list=[] # [[],[]...]
        for j in scene[i]:
            # print(j)
            if (j == "file"):
                # print(scene[i][j])
                imgs=(scene[i][j].split("https://"))
                r=[s for s in imgs if ".jpg" in s or ".JPG" in s]
                img="https://"+" https://".join(r)
                # img_list.append(img)
                # print(img_list)
        one_csv_data.append(img)
        csv_data.append(one_csv_data)
    return head_csv,csv_data

# data=get_data()
# print(get_data()[0])

"""[b]資料存到csv
"""
with open("D:/MySQL Server 8.0/Uploads/data.csv", mode="w", encoding="UTF-8-SIG", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(get_data()[0]) # 寫入head_csv[]
    # quoting: 碰到特殊符號(,、。；)不會導致換單元格...等操作
    # delimiter: 只有csv_data[]的分割符有換單元格的效果
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL,delimiter=',')
    writer.writerows(get_data()[1]) # 寫入csv_data[]
    print("資料匯入完成")

"""3. 存到mysql裡 > [a]head_csv製作初始sql(創建表格)
"""
def table_sql():
    tables=[]
    fields=[]
    for i in get_data()[0]:
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
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
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


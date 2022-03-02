""" Part 1 - 1：將景點資料存放至資料庫
    1. 抓取所有景點資料(with開啟資料 > json法方讀取)
    2. 處理資料 & 過濾圖片後綴名.jpg(for loop)
    3. 存到mysql裡(json, csv, pandas?, numpy?, ...)
"""
import json
import mysql.connector
from mysql.connector import errors
import csv

with open("taipei-attractions.json", mode="r", encoding="UTF-8") as file:
    data_json=json.load(file)
    # print(data)
# 景點資訊(全部)
scene=data_json["result"]["results"]

def get_data():

    # 存储数据用的列表
    csv_data = []
    # 表头，自己需要的数据项
    head_csv = ["stitle", "CAT2", "xbody", "address", "info", "MRT", "latitude", "longitude", "file"]
        
    # 循环遍历每条数据，取出自己需要的数据
    for i in scene:
        one_csv_data = []
        # one_csv_data.append(i["_id"])
        one_csv_data.append(i["stitle"])
        one_csv_data.append(i["CAT2"])
        one_csv_data.append(i["xbody"])
        one_csv_data.append(i["address"])
        one_csv_data.append(i["info"])
        one_csv_data.append(i["MRT"])
        one_csv_data.append(i["latitude"])
        one_csv_data.append(i["longitude"])
        one_csv_data.append(i["file"])
        csv_data.append(one_csv_data)
    return head_csv,csv_data

data=get_data()

print(get_data()[0])

with open("data.csv", mode="w", encoding="UTF-8-SIG", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(get_data()[0])
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL,delimiter=',')
    writer.writerows(get_data()[1])

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
print(table_sql()[0])


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
    sql="""LOAD DATA INFILE  'D:/MySQL Server 8.0/Uploads/data.csv'
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


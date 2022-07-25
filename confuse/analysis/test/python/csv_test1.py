import json
import mysql.connector
from mysql.connector import errors

# (a)打開json > 讀取內容
with open("../data/taipei-attractions.json", mode="r", encoding="UTF-8-SIG") as file:
    # data=file.read()
    data=json.load(file)
# 印出 results 第一個
# print(data["result"]["results"][0])

# (b)json資料 > 處理
# 景點資訊
attractions=data["result"]["results"]
# print(attractions)

def table():
    tables=[]
    fields=[]
    for i in attractions[0]:
        if i == "longitude" or i == "latitude":
            fields.append(i)
            char=i+" FLOAT"
            tables.append(char)
        elif i == "file" or i == "xbody":
            fields.append(i)
            char=i+" TEXT"
            tables.append(char)
        else:
            fields.append(i)
            char=i+" VARCHAR(255)"
            tables.append(char)

    tables_sql = ','.join(tables)
    # print(tables)
    sql="CREATE TABLE IF NOT EXISTS `scenery`"+"("+tables_sql+", PRIMARY KEY(_id)"+");"
    return sql,fields

# print(table()[1])

with open("D:/MySQL Server 8.0/Uploads/data.csv", mode="w", encoding="UTF-8-SIG") as csvfile:
    import pandas as pd
    result = pd.read_csv(csvfile, sep=',', header=None)  # 包括第一行
    # result = pd.read_csv(csvfile, sep=',')               # 不包括第一行
    print(result)
    
    # for i in range(5):
    #     if i != 0:
    #         print("---------------------------")
    #         csvfile.write("\n")
    #     for j in attractions[i]:
    #         print(attractions[i][j])
    #         csvfile.write(str(attractions[i][j])+",")

# try:
#     conn=mysql.connector.connect(option_files="my.conf")
#     cnx=conn.cursor()
#     print(conn.connection_id)
#     sql=table()
#     cnx.execute(sql)
#     print("創建表格")
#     sql1="LOAD DATA INFILE 'D:/MySQL Server 8.0/Uploads/data.csv' INTO TABLE scenery FIELDS TERMINATED BY ',';"
#     cnx.execute(sql1)
#     print("新增資料")
# except errors.Error as e:
#     print(e)
# finally:
#     conn.commit()
#     cnx.close()
#     conn.close()
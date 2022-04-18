import os
from dotenv import load_dotenv
import mysql.connector.pooling

load_dotenv()

dbconfig={
    "host":os.getenv("HOST"),
    "port":os.getenv("PORT"),
    "user":os.getenv("USER"),
    "password":os.getenv("PASSWORD"),
    "database":os.getenv("DATABASE")
}

class MySQLPool:
    # [初始化] 傳入變量(Variables)
    def __init__(self, pool_name="mypool", pool_size=5, **dbconfig):
        self.dbconfig=dbconfig
        self.pool=self.create_pool(pool_name=pool_name, pool_size=pool_size)
        
    # [創建連接池] 根據傳入參數(Method)
    def create_pool(self, pool_name="mypool", pool_size=5):
        pool=mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=True,
            **self.dbconfig
        )
        return pool
    
    # [關閉] 鼠標 & 連接
    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    def error_massage(self,massage):
        return {
                "error": True,
                "message": massage
                }

    # [傳入] sql, val, commit(沒有的話使用預設值)
    # [判斷] 是否有val & 是否commit
    # [執行] 返回結果
    def execute(self, sql, val=None, commit=None):
        try:
            conn=self.pool.get_connection()
            print("連接數據庫: ", conn.connection_id)
            cursor=conn.cursor()
            if val:
                cursor.execute(sql, val)
            else:
                cursor.execute(sql)

            if commit is True:
                conn.commit()
                return None
            else:
                res=cursor.fetchall()
                return res
        except Exception as e:
            print(e)
            res=self.error_massage("伺服器錯誤")
            return res
        finally:
            if conn.in_transaction:
                conn.rollback()
            self.close(conn, cursor)


"""/pool=mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)

conn=pool.get_connection()

if conn.is_connected():
    db_Info = conn.get_server_info()
    print("Connected to MySQL database... MySQL Server version on ",db_Info)
print("連接數據庫完成: ", conn.connection_id)
cnx=conn.cursor(dictionary=True)

if __name__ == "__main__":
    print(dbconfig)
    mysql_pool=MySQLPool(**dbconfig)
    sql="select id,stitle from scnery"
    print(mysql_pool.execute(sql))
"""

import mysql.connector.pooling

dbconfig={
    "host":"db",
    # "host":"localhost",
    "user":"root",
    "password":"0973",
    "database":"taipei_trip",
    "port": "3306"
}
pool=mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)


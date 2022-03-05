import mysql.connector.pooling

dbconfig={
    "host":"localhost",
    "user":"root",
    "password":"0973",
    "database":"taipei_trip"
}
pool=mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **dbconfig
)


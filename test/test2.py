
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
        # one_csv_data.append(1 if i["raceState"]=="ONGOING" else 0)
        one_csv_data.append(i["MRT"])
        one_csv_data.append(i["latitude"])
        one_csv_data.append(i["longitude"])
        one_csv_data.append(i["file"])
        # one_csv_data.append("人民币" if i["currencySymbol"]=="￥" else "美元")
        csv_data.append(one_csv_data)
    return head_csv,csv_data

data=get_data()

'''
将列表数据存储为csv格式文件
'''
def save_to_cvs(data):
    # 解析数据
    head_csv = data[0] # 表头
    csv_data = data[1] # 表中数据
    # 将数据转化成DataFrame格式
    csv_data =pd.DataFrame(columns=head_csv,data=csv_data,)
    # print(csv_data)
    # 调用to_csv函数将数据存储为CSV文件
    csv_data.to_csv('data.csv',index=False, encoding='UTF-8-SIG')
    
save_to_cvs(data)

'''
新建一个数据库
'''
def create_database(database, cursor):
    # 创建database, 如果存在则删除database，然后新建一个
    cursor.execute("drop database if exists %s;"%database)
    cursor.execute("create database %s;"%database)
    print("成功创建数据库：%s"%database)
    
'''
在制定数据库中新建一个数据表
'''
def create_table(table_name, table_sql, database, cursor):
    # 选择 database 数据库
    cursor.execute("use %s;"%database)
    # 创建一个名为table的数据库
    # 如果存在table这个表则删除
    cursor.execute("drop table if exists %s;"%table_name)
    # 创建table表
    cursor.execute(table_sql)
    print("成功在数据库{0}中创建数据表：{1}".format(database,table_name))
    

'''
在指定数据库的数据表中增、删、查、改
'''
def sql_basic_operation(table_sql, database, cursor):
    # 选择 database 数据库
    cursor.execute("use %s"%database)
    # 执行sql语句
    cursor.execute(table_sql)
    print("sql语句执行成功")

# 连接数据库 并添加cursor游标
conn = mysql.connector.connect(option_files="my.conf")
cursor = conn.cursor()
# 数据表名称
database="taipei_trip"
# 创建数据库
create_database(database, cursor)

table_name = "scenery"
#  创建数据表，设置raceId为主键
table_sql = """create table %s(
                id int not null auto_increment,
                stitle varchar(255),
                CAT2 varchar(255),
                xbody text,
                address varchar(255),
                info text,
                MRT varchar(255),
                latitude float,
                longitude float,
                file text,
                PRIMARY KEY(id));
                """%table_name
create_table(table_name, table_sql, database, cursor)

'''
读取csv文件数据
'''
def read_csv(filepath):
    # 读取csv文件，直接调用pandas的read_csv函数即可
    data = pd.read_csv(filepath, encoding='UTF-8')
    # print(type(data)) # <class 'pandas.core.frame.DataFrame'>
    sql_data = []
    # 遍历DataFrame格式数据，取出一行行的数据
    for row in data.itertuples():
        # print(type(row))  # <class 'pandas.core.frame.Pandas'>
        # print(getattr(row,'raceName')) # 零基础入门推荐系统 - 新闻推荐
        sql_data.append((getattr(row,'stitle'), getattr(row,'CAT2'), getattr(row,'xbody'), getattr(row,'address'), getattr(row,'info'),
                        getattr(row,'MRT'), getattr(row,'latitude'), getattr(row,'longitude'), getattr(row,'file'), ","))
    return sql_data

filepath = 'data.csv'
sql_data = read_csv(filepath)

print(sql_data)

# # 循环插入数据
# for row in sql_data:
#     # 拼接插入sql语句
#     sql_insert = '''insert into {0} values({1},'{2}','{3}','{4}','{5}',{6},{7},{8},{9});
#     '''.format(table_name,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8])                                                                                    
#     # print(sql_insert)
#     cursor.execute(sql_insert, database, cursor)
    
# conn.commit()

sql="""
        insert into '%s' value('%s','%s','%s','%s','%s','%s','%s','%s','%s')
    """%(sql_data)
cursor.execute(sql)

conn.commit()
# 关闭连接
conn.close()
cursor.close()
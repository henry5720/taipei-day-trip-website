"""[測試] mysql > sql指令 && json
"""

from flask import *
import json
str1="1 2 3 4 5"
records={"id":1,"a":"12345"}

# print(str1.split())
# print(json.dumps(data))
# print(list(records["a"]))



# for i in records["a"]:
# #     dict1={}
#     dict2={}
# #     list1=[]
#     # dict2["id"]=i["id"]
#     dict2["name"]=list(records["a"])
#     print(dict2)
#     # dict2["images"][list1]=i["file"]
w="溫泉"
sql="select ,stitle from scenery where stitle like '%'"+w+"%;"
sal1="select id,stitle from scenery where"


sql="""
        SELECT CONCAT('[',
        json_object(
            'id', id,
            'name', stitle,
            'category', CAT2,
            'description', xbody,
            'address', address,
            'transport', info,
            'mrt', MRT,
            'latitude', latitude,
            'longitude', longitude
            
            ),']')
        as data FROM scenery limit 1;
    """
dict2={}
s="https://www.travel.taipei/d_upload_ttn/sceneadmin/pic/11003993.jpg https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D457/E341/F171/f6dc25a6-cc44-4e4d-a7ea-aea011e2aa65.jpg https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D375/E862/F67/dcada704-a151-4b49-ac44-a349e7761973.jpg https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D293/E834/F864/7493ca40-985e-4d7e-9340-f738b6096c26.jpg https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D988/E745/F29/cc1e0a3a-0e3c-47dc-88b8-9c7a9ddc606e.jpg https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C0/D37/E611/F805/ec29667c-0ff6-435a-ab82-2905492d04fc.jpg https://www.travel.taipei/d_upload_ttn/sceneadmin/image/A0/B0/C1/D202/E23/F478/a219480b-2bb0-4e80-9069-2704c7904545.jpg"

dict2["images"]=s.split()
# print(dict2)
    # 'images', file,

keyword="水"
page="1"
def get_sql(keyword,page):
    sql="""select id,stitle 
        from scenery 
        where stitle 
        like '%"""+keyword+"""
        %' limit 12 offset"""+page+";"
    print(sql)
    return sql
get_sql(keyword,page)


# dict & list (for flask json)
dict1={} # dict(第1層)
list1=[] # dict(第1層) > list(第1層)
# 遍歷資料
for i in records:
    dict2={} # dict(第2層)
    # print(type(i))
    dict2["id"]=i["id"]
    dict2["name"]=i["stitle"]
    dict2["category"]=i["CAT2"]
    dict2["description"]=i["xbody"]
    dict2["address"]=i["address"]
    dict2["transport"]=i["info"]
    dict2["mrt"]=i["MRT"]
    dict2["latitude"]=i["latitude"]
    dict2["longitude"]=i["longitude"]
    dict2["images"]=i["file"].split()
    list1.append(dict2)
    dict1["data"]=list1
    
    # print(json.dumps(i["stitle"]))
    # print(i["file"].split())
    # print(type(i["file"
# print(dict1)
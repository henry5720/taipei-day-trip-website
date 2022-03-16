import json
import csv

"""1. 抓取所有景點資料(with開啟資料 > json法方讀取)
"""
with open("../data/taipei-attractions.json", mode="r", encoding="UTF-8") as file:
    data_json=json.load(file)
    # print(data)

# 景點資訊(全部)
scene=data_json["result"]["results"]

# 表頭, 所需數據名
head_csv = ["stitle", "CAT2", "xbody", "address", "info", "MRT", "latitude", "longitude", "file"]
csv_data = [] # 存數據的列表

def img_list():
    img_list=[] # [[],[]...]
    for i in range(1):
        imgs=(scene[i]["file"].split("https://"))
        r=[s for s in imgs if ".jpg" in s or ".JPG" in s]
        img="https://"+",https://".join(r)
        img_list.append(img)
        # print(img_list)
    print("圖片篩選完成")
    return img_list
# print(img_list())
# 循環遍歷json(value),增加到csv_data
for i in range(len(scene)):
    # 存單項數據的列表,循環記錄一次後,再設為空列表[]
    print(i)
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
    img_list=[] # [[],[]...]
    for j in scene[i]:
        # print(j)
        if (j == "file"):
            # print(scene[i][j])
            imgs=(scene[i][j].split("https://"))
            r=[s for s in imgs if ".jpg" in s or ".JPG" in s]
            img="https://"+",https://".join(r)
            img_list.append(img)
            # print(img_list)
    # print("圖片篩選完成")

    one_csv_data.append(img_list)
    csv_data.append(one_csv_data)


print(csv_data)

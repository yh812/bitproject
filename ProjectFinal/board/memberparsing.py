#!/usr/bin/python3

import sys
import json
from collections import OrderedDict

f= open('member.txt','r',encoding='utf-8')
for i in f.readlines():
    item = i.split(",")
    file_data = OrderedDict()
    
    file_data["id"] = item[0]
    file_data["userid"] = item[1]
    file_data["nickname"] = item[2]
    file_data["passwd"] = item[3]
    file_data["tel"] = item[4]
    file_data["email"] = item[6]
    file_data["gender"] = item[7]
    file_data["generation"] = item[8]
    file_data["birth"] = item[9]
    file_data["userimage"] = item[10]
    file_data["user_total_point"] = item[11]
    file_data["user_current_point"] = item[12]
    file_data["regdate"] = item[13]
    file_data["address"] = item[14]
    file_data["address2"] = item[15]
    file_data["sosial"] = item[16]
    file_data["userimg"] = item[17]
    
    with open("member.json", "a+", encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False)
#!/usr/bin/python3

import sys
import json
from collections import OrderedDict

f= open('polls.txt','r',encoding='utf-8')
for i in f.readlines():
    item = i.split(",")
    file_data = OrderedDict()
    
    file_data["id"] = item[0]
    file_data["bs_id_id"] = item[1]
    file_data["choice_text_name_id"] = item[2]
    file_data["question_name_id"] = item[3]
    
    
    with open("polls.json", "a+", encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False)
import os
import json
import pathlib
from pathlib import Path
import csv


target_string="ParIndex"
directory_path=Path(os.getcwd())
return_list=[]
for file in directory_path.iterdir():
    if target_string in file.name:
        print(file.name)
        fo = open(file,"r")
        json_content = json.load(fo)
        word_list=sorted(json_content.keys())
        return_list.append(word_list)  
         


with open("index_of_indexes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(return_list)
        
        
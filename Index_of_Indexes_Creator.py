import os
import json
import pathlib
from pathlib import Path

def index_maker(file):
    word_location={}
    reader = open(file,"r", encoding="utf-8")
    length_start=0
    for lines in reader:
        line=lines.split(",")[0]
        line2=line.replace("[","")
        line2=line2.replace("\"","")
        word_location[line2]=length_start
        length_start+=len(lines)+1
    return word_location

dictionary_of_Terms = index_maker("fullIndex.json")

'''target_string="ParIndex"
directory_path=Path(os.getcwd())
return_list=[]

for file in directory_path.iterdir():
    if target_string in file.name:
        print(file.name)

        return_list.append(dictionary_of_Terms)'''
    
with open("index_of_indexes.json", "w", encoding="utf-8") as f:
    json.dump(dictionary_of_Terms, f, indent = 1)

print("Done!")
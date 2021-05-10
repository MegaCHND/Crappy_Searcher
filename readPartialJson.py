import os 
import json 

fo = open("ParIndex1.json","r")
JsonContent = json.load(fo)
x = sorted(JsonContent.keys())
print(x)
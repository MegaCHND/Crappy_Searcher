import os
import re
import json
from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer

#global vars tha can be changed
dict_of_Words = dict()
text = ""

#Vars that should never be changed
CurrDirectory = os.getcwd()
directory_in_str = '\Testo'
directory = os.fsencode(CurrDirectory + directory_in_str)
ps = SnowballStemmer('english')
tag_names = ["h1","h2","h3","h4","h5","h6","title","p"]


def wordCollector(soup):
    global dict_of_Words
    global text 
    text = soup.get_text(" ")
    tag_list=soup.find_all()
    for tag in tag_list:
        if tag.name in tag_names:
            print(tag.text)
    text = re.sub(r'[^a-zA-Z0-9 ]','', text).lower()
    for i in text.split():
        i = ps.stem(i)
        dict_of_Words[i]=dict_of_Words.get(i,0)+1

def soupfyHtml(content):
    soup = BeautifulSoup(content, "lxml")
    wordCollector(soup)

def openFile(subdir,file):
    FullFilePath = os.fsdecode(os.path.join(subdir, file))
    OpenedFile = open(FullFilePath, "r")
    JsonContent = json.load(OpenedFile)
    HtmlContent = JsonContent["content"]
    soupfyHtml(HtmlContent)

def printReport():
    reportFile = open("report.txt", "w", encoding="utf-8")
    #reportFile.write(text)
    reportFile.write("Words found\n")
    for val in sorted(dict_of_Words, key=dict_of_Words.get, reverse=True):
        reportFile.write(str(val)+", Times seen: "+str(dict_of_Words[val])+"\n")


for subdir, dirs, files in os.walk(directory):
     for file in files:
        openFile(subdir,file)

printReport()

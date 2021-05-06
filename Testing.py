import os
import re
import json
import csv #using csv to read and write to temp invertedIndex since it is much faster
#import pandas as pd #using pandas to compress duplicates in the inverted Index since it is much faster than csv
from functools import reduce
from bs4 import BeautifulSoup
from collections import Counter
from nltk.stem import SnowballStemmer

#global vars tha can be changed
#dict_of_Words = dict()
CurrUrl = ""
CurrFilePath = ""
partialInvertedIndex = {}
#Vars that should never be changed
CurrDirectory = os.getcwd()
directory_in_str = '\dev2'
directory = os.fsencode(CurrDirectory + directory_in_str)
ps = SnowballStemmer('english')
tag_names = ["h1","h2","h3","h4","h5","h6","title","p"]


def wordCollector(soup):
    global CurrUrl
    global CurrFilePath
    global partialInvertedIndex
    print(CurrFilePath)
    text = ""
    text = soup.get_text(" ")
    #tag_list=soup.find_all()
    text = re.sub(r'[^a-zA-Z0-9 ]','', text).lower()
    text = remov_duplicates(text)
    for i in text.split():
        i = ps.stem(i)
        if(i not in partialInvertedIndex.keys()):
            partialInvertedIndex[i] = {}
            partialInvertedIndex[i]["Urls"] = []
            partialInvertedIndex[i]["Filepaths"] = []
        partialInvertedIndex[i]["Urls"]+= [CurrUrl]
        partialInvertedIndex[i]["Filepaths"] += [CurrFilePath]
    

def remov_duplicates(st):
   Pattern = r"\b(\w+)(?:\W\1\b)+"
   return re.sub(Pattern, r"\1", st)

def soupfyHtml(content):
    soup = BeautifulSoup(content, "lxml")
    wordCollector(soup)

def openFile(subdir,file):
    global CurrFilePath
    global CurrUrl
    CurrFilePath = os.fsdecode(os.path.join(subdir, file))
    OpenedFile = open(CurrFilePath, "r")
    JsonContent = json.load(OpenedFile)
    HtmlContent = JsonContent["content"]
    CurrUrl = JsonContent["url"]
    soupfyHtml(HtmlContent)

def printReport():
    reportFile = open("report.txt", "w", encoding="utf-8")
    #reportFile.write(text)
    reportFile.write("Words found\n")
    for val in sorted(dict_of_Words, key=dict_of_Words.get, reverse=True):
        reportFile.write(str(val)+", Times seen: "+str(dict_of_Words[val])+"\n")


def WriteToInvertedIndex(pII):
    with open('InvertedIndex.csv', 'w') as Iindex:

        #declaring the fieldnames for the CSV file
        fieldNames = ['word', 'Urls', 'Filepaths']

        #creating a DictWriter object
        csvWriter = csv.DictWriter(Iindex, fieldnames= fieldNames)

        #writing the header
        csvWriter.writeheader()

        for word, fileDetails in pII.items():

            #creating a string of all the file names and file paths
            fileUrlString = reduce(lambda x, y: x + ", " + y, fileDetails['Urls'])
            filePathString = reduce(lambda  x, y: x + ", " + y, fileDetails['Filepaths'])

            #writing the row
            csvWriter.writerow({'word': word, 'Urls': fileUrlString, 'Filepaths': filePathString})

for subdir, dirs, files in os.walk(directory):
     for file in files:
        openFile(subdir,file)
WriteToInvertedIndex(partialInvertedIndex)
print("done!")
#printReport()

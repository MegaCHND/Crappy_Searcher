import os 
from collections import defaultdict
from bs4 import BeautifulSoup
import re 
import traceback 
import json 
import math 
from nltk.stem import SnowballStemmer 

#Since we'll need to rank words for searching later, might as well try to do so now
#I chose strong, b, bold, h1-3, and title. I didn't include h4-6 b/c the text shrinks back to normal the closer you get to 6
#p isn't special b/c the prof didn't include it in his list in the assignment =p
SPECIAL_TAG_FACTORS = {
    "strong": 1.2,
    "b": 1.2,
    "bold": 1.2,
    "h1": 1.4,
    "h2": 1.3,
    "h3": 1.25,
    "title": 1.5,
}

#Made classes for the inverted index to use
#Posting contains the tf score as well as the specail tags used (if the word was in any)
class Posting:
    def __init__(self):
        self.tf = 0
        self.special_tags = set()
        
#Data contains the posting as well as the idf score for the word
class Data:
    def __init__(self):
        self.idf = 0
        self.postings = defaultdict(Posting)
        
class InvertedIndex:
    def __init__(self):
        self.dictionary = defaultdict(Data)
        self.num_doc_ids = 0
    def __getitem__(self, term):
        return self.dictionary[term]
    def __setitem__(self, term, data):
        self.dictionary[term] = data
    def get_number_of_words(self):
        return len(self.dictionary.keys())
    def items(self):
        return self.dictionary.items()
    def get_Full_Index(self, outfile):
        j = dict()
        for term, data in self.dictionary.items():
            j[term] = dict()
            j[term]["idf"] = data.idf
            j[term]["postings"] = dict()
            for docID, posting in data.postings.items():
                j[term]["postings"][docID] = dict()
                j[term]["postings"][docID]["tf"] = posting.tf
                j[term]["postings"][docID]["special_tags"] = list(posting.special_tags)
        json.dump(j, outfile, indent = 4)
    def print_report(self, outfile):
        outfile.write("Words Found \n")
        outfile.write(str(self.get_number_of_words()))
        outfile.write("\nNumber of indexed documents \n")
        outfile.write(str(self.num_doc_ids))

def tokenize(html, docID):
    print("tokenizing " + docID)
    global index
    global ps
    soup = BeautifulSoup(html, 'lxml')
    special_tags = soup.find_all(["strong", "b", "bold", "h1", "h2", "h3", "title"])
    for special_tag in special_tags:
        special_tag_content = special_tag.get_text().strip()
        tokens = re.split('\W+', special_tag_content)
        for token in tokens:
            if token != "":
                token = ps.stem(token)
                index[token].postings[docID].tf += 1
                index[token].postings[docID].special_tags.add(special_tag.name)

def openFile(subdir,file):
    global CurrFilePath
    CurrFilePath = os.fsdecode(os.path.join(subdir, file))
    OpenedFile = open(CurrFilePath, "r")
    JsonContent = json.load(OpenedFile)
    HtmlContent = JsonContent["content"]
    CurrUrl = JsonContent["url"]
    tokenize(HtmlContent, CurrUrl)

index = InvertedIndex();
CurrDirectory = os.getcwd()
directory_in_str = '\developer'
directory = os.fsencode(CurrDirectory + directory_in_str)
CurrFilePath = ""
ps = SnowballStemmer('english')

try:
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            openFile(subdir,file)
            index.num_doc_ids += 1
    for term, data in index.items():
        #after the index is made, I go back and calculate the idf vals for every word (technically stem)
        data.idf = index.num_doc_ids/float(len(data.postings))
except:
    traceback.print_exc()
    
#Here I print stuff for M1 report
reportFile = open("report.txt" , "w") 
indexFile = open("index.json", "w")   
index.get_Full_Index(indexFile)
index.print_report(reportFile)
reportFile.close()
indexFile.close()

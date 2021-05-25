import os 
import re 
import traceback 
import json 
import math 
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import SnowballStemmer
from urllib.parse import urlparse,urldefrag

#Made classes for the inverted index to use
#Posting contains the tf score as well as the specail tags used (if the word was in any)
class Posting:
    def __init__(self):
        self.tf = 0
        self.special_tags = set()
        self.position = 0
        
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
        for term, data in sorted(self.dictionary.items()):
            j[term] = dict()
            j[term]["idf"] = data.idf
            j[term]["postings"] = dict()
            for docID, posting in data.postings.items():
                j[term]["postings"][docID] = dict()
                j[term]["postings"][docID]["tf"] = posting.tf
                j[term]["postings"][docID]["special_tags"] = list(posting.special_tags)
                j[term]["postings"][docID]["position"] = posting.position
        for i in j.items():
            outfile.write(json.dumps(i))
            outfile.write('\n')
    '''def print_report(self, outfile):
        outfile.write("Words Found \n")
        outfile.write(str(self.get_number_of_words()))
        outfile.write("\nNumber of indexed documents \n")
        outfile.write(str(self.num_doc_ids))'''
    def wipe(self):
        self.dictionary.clear()
        self.num_doc_ids = 0

def tokenize(html, docID):
    print("tokenizing " + docID)
    global index
    global ps
    soup = BeautifulSoup(html, 'lxml')
    special_tags = soup.find_all(["strong", "b", "bold", "h1", "h2", "h3", "title"])
    token_position = 1
    for special_tag in special_tags:
        special_tag_content = special_tag.get_text().strip()
        tokens = re.split('\W+', special_tag_content)
        for token in tokens:
            if token != "":
                token = ps.stem(token)
                index[token].postings[docID].tf += 1
                index[token].postings[docID].special_tags.add(special_tag.name)
                index[token].postings[docID].position = token_position
                token_position += 1

def openFile(subdir,file):
    global CurrFilePath
    global Dict_of_Urls
    CurrFilePath = os.fsdecode(os.path.join(subdir, file))
    OpenedFile = open(CurrFilePath, "r", encoding="utf-8")
    JsonContent = json.load(OpenedFile)
    HtmlContent = JsonContent["content"]
    CurrUrl = JsonContent["url"]
    defragedUrl = urldefrag(CurrUrl)[0]
    if defragedUrl not in Dict_of_Urls:
        Dict_of_Urls[defragedUrl] = Dict_of_Urls.get(defragedUrl, 0) + 1
        tokenize(HtmlContent, CurrUrl)

def dumpIt():
    global counterOfMadeIndexes
    global indexNameOfFile
    global index
    print("Dumping")
    indexFile = indexNameOfFile+str(counterOfMadeIndexes)+".json"
    indexF = open(indexFile, "w")   
    index.get_Full_Index(indexF)
    indexF.close()
    
if __name__ == '__main__':    
    index = InvertedIndex();
    CurrDirectory = os.getcwd()
    directory_in_str = '\Testo'
    directory = os.fsencode(CurrDirectory + directory_in_str)
    CurrFilePath = ""
    ps = SnowballStemmer('english')
    Dict_of_Urls = {}
    indexNameOfFile = "ParIndex"
    counterOfMadeIndexes = 0

    try:
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if index.num_doc_ids <= 10000:
                    openFile(subdir,file)
                    index.num_doc_ids += 1
                else:
                    for term, data in index.items():
                        #after the index is made, I go back and calculate the idf vals for every word (technically stem)
                        data.idf = math.log(index.num_doc_ids/float(len(data.postings)))
                    dumpIt()
                    counterOfMadeIndexes += 1
                    index.wipe()
        
        #computing last set of idf's before the final data dump
        for term, data in index.items():
            #after the index is made, I go back and calculate the idf vals for every word (technically stem)
            data.idf = math.log(index.num_doc_ids/float(len(data.postings)))
        dumpIt()
        index.wipe()

    except:
        traceback.print_exc()


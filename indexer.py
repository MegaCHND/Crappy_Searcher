import os 
import re 
import traceback 
import json 
import math 
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import SnowballStemmer
from urllib.parse import urlparse,urldefrag

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
    def wipe(self):
        self.dictionary.clear()
        self.num_doc_ids = 0

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
    global Dict_of_Urls
    CurrFilePath = os.fsdecode(os.path.join(subdir, file))
    OpenedFile = open(CurrFilePath, "r")
    JsonContent = json.load(OpenedFile)
    HtmlContent = JsonContent["content"]
    CurrUrl = JsonContent["url"]
    defragedUrl = urldefrag(CurrUrl)[0]
    if defragedUrl not in Dict_of_Urls:
        Dict_of_Urls[defragedUrl] = Dict_of_Urls.get(defragedUrl, 0) + 1
        tokenize(HtmlContent, CurrUrl)

def dumpIt():
    #Here I print stuff for M1 report
    global counterOfMadeIndexes
    global indexNameOfFile
    global index
    indexFile = indexNameOfFile+str(counterOfMadeIndexes)+".json"
    indexF = open(indexFile, "w")   
    index.get_Full_Index(indexF)
    indexF.close()
    
index = InvertedIndex();
CurrDirectory = os.getcwd()
directory_in_str = '\dev2'
directory = os.fsencode(CurrDirectory + directory_in_str)
stop_words = {"a","about","above","after","again","against","all","am","an","and","any","are","arent","as","at","be","because","been","before","being","below","between","both","but","by","cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll","youre","youve","your","yours","yourself","yourselves"}
CurrFilePath = ""
ps = SnowballStemmer('english')
Dict_of_Urls = {}
indexNameOfFile = "ParIndex"
counterOfMadeIndexes = 0

try:
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if index.num_doc_ids <= 500:
                openFile(subdir,file)
                index.num_doc_ids += 1
            else:
                print("Dumping")
                dumpIt()
                counterOfMadeIndexes += 1
                index.wipe()
                
    for term, data in index.items():
        #after the index is made, I go back and calculate the idf vals for every word (technically stem)
        data.idf = index.num_doc_ids/float(len(data.postings))
except:
    traceback.print_exc()
    
dumpIt()
reportFile = open("report.txt" , "w") 
index.print_report(reportFile)
reportFile.close()
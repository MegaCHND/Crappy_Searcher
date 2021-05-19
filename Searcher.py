import csv
import json 
import indexer
import math
import time 
from collections import defaultdict
from nltk.stem import SnowballStemmer

SPECIAL_TAG_FACTORS = {
    "strong": 1.2,
    "b": 1.2,
    "bold": 1.2,
    "h1": 1.4,
    "h2": 1.3,
    "h3": 1.25,
    "title": 1.5,
}

indexNameOfFile = "ParIndex"
stop_words = {"a","about","above","after","again","against","all","am","an","and","any","are","arent","as","at","be","because","been","before","being","below","between","both","but","by","cant","cannot","could","couldnt","did","didnt","do","does","doesnt","doing","dont","down","during","each","few","for","from","further","had","hadnt","has","hasnt","have","havent","having","he","hed","hell","hes","her","here","heres","hers","herself","him","himself","his","how","hows","i","id","ill","im","ive","if","in","into","is","isnt","it","its","its","itself","lets","me","more","most","mustnt","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell","shes","should","shouldnt","so","some","such","than","that","thats","the","their","theirs","them","themselves","then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to","too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","what","whats","when","whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","would","wouldnt","you","youd","youll","youre","youve","your","yours","yourself","yourselves"}
miniIndex = indexer.InvertedIndex()
ps = SnowballStemmer('english')
csv_file = open('index_of_indexes.csv', "r", encoding="utf-8")
csv_reader = csv.reader(csv_file, delimiter=',')
csv_rows = []
for row in csv_reader:
    csv_rows.append(row)

def get_results(query, num_results_to_show):
    global miniIndex
    score = defaultdict(float)
    tic = time.perf_counter()
    for token in query.split(" "):
        print("token is " + token)
        if token not in stop_words:
            token = ps.stem(token)
            grab_records(token)
            for docID, posting in miniIndex[token].postings.items():
                constant_factor = 1
                for special_tag in posting["special_tags"]:
                    constant_factor *= SPECIAL_TAG_FACTORS[special_tag]
                score[docID] += constant_factor * (1 + math.log(posting["tf"]) * math.log(miniIndex[token].idf))
    sorted_keys = sorted(score.keys(), reverse=True, key=lambda k : score[k])
    results = []
    i = 0
    for key in sorted_keys:
        if i < num_results_to_show:
            results.append(key)
            i += 1
        else:
            break
    toc = time.perf_counter()
    print("Query is " + query)
    print(f"Found results in {toc - tic:0.4f} seconds")
    miniIndex.wipe()
    return results


def grab_records(word):
    global miniIndex
    global csv_rows
    list_of_miniIndexes = []
    line_count = 0    
    
    for row in csv_rows:
        if (word in row):
            list_of_miniIndexes.append(line_count)
        line_count += 1
    print("list_of_miniIndexes is:")
    print(list_of_miniIndexes)
    
    for indexNum in list_of_miniIndexes:
        miniIndexName = indexNameOfFile+str(indexNum)+".json"
        miniIndexFile = open(miniIndexName, "r")
        miniIndexJson = json.load(miniIndexFile)
        miniIndex[word].idf += miniIndexJson[word]["idf"]
        miniIndex[word].postings.update(miniIndexJson[word]["postings"])
    
    if(len(list_of_miniIndexes)>0):
        miniIndex[word].idf = miniIndex[word].idf/len(list_of_miniIndexes)
    
    print(miniIndex[word].postings)
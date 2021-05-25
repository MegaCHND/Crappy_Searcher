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
json_index_file = open('index_of_indexes.json', "r", encoding="utf-8")
FullIndexFile = open("fullIndex.json", "r", encoding="utf-8")
ListOfDicts = json.load(json_index_file)


def get_results(query, num_results_to_show):
    global miniIndex
    score = defaultdict(float)
    print("query is " + query)
    tic = time.perf_counter()
    for token in query.split(" "):
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
    print(f"Found results in {toc - tic:0.4f} seconds")
    miniIndex.wipe()
    return results


def grab_records(word):
    global miniIndex
    Word_exists_count = 0
    word_pos = 0
    if(ListOfDicts.get(word) is not None):
        word_pos = ListOfDicts[word]
        FullIndexFile.seek(word_pos)
        data = FullIndexFile.readline() 
        miniIndexJson = json.loads(data)
        miniIndex[word].idf += miniIndexJson[1]["idf"]
        miniIndex[word].postings.update(miniIndexJson[1]["postings"])
    '''for indexNum in range(len(ListOfDicts)):
        if(ListOfDicts[indexNum].get(word) is not None):
            miniIndexName = indexNameOfFile+str(indexNum)+".json"
            miniIndexFile = open(miniIndexName, "r")
            word_pos = ListOfDicts[indexNum][word]
            miniIndexFile.seek(word_pos)
            data = miniIndexFile.readline() 
            miniIndexJson = json.loads(data)
            miniIndex[word].idf += miniIndexJson[1]["idf"]
            miniIndex[word].postings.update(miniIndexJson[1]["postings"])
            Word_exists_count += 1
    
    if(Word_exists_count > 0):
        miniIndex[word].idf = miniIndex[word].idf/Word_exists_count'''
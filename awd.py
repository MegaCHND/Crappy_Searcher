import csv
import json 
import indexer

indexNameOfFile = "ParIndex"
list_of_indexes = []
index = indexer.InvertedIndex()
with open('index_of_indexes.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0    
    for row in csv_reader:
        if ("uci" in row):
            list_of_indexes.append(line_count)
        line_count += 1
    print(f'Processed {line_count} lines.')
    print(list_of_indexes)


for indexNum in list_of_indexes:
    indexName = indexNameOfFile+str(indexNum)+".json"
    indexFile = open(indexName, "r")
    indexJson = json.load(indexFile)
    index["uci"].idf += indexJson["uci"]["idf"]
    index["uci"].postings.update(indexJson["uci"]["postings"])
    #print(indexJson["uci"]["postings"])
    
index["uci"].idf = index["uci"].idf/len(list_of_indexes)
print(index["uci"].idf  )
#print(index["uci"].postings)
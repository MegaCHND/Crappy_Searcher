import mmap
import json
import os
import pathlib
from pathlib import Path

target_string="ParIndex"
directory_path=Path(os.getcwd())
num_of_Index = 0

for file in directory_path.iterdir():
    if target_string in file.name:
        num_of_Index+=1

        
lastIter=num_of_Index-1

for i in range(1,num_of_Index):
    if(i == 1):
        part0=open('ParIndex0.json', "r", encoding="utf-8")
        nextIndex='ParIndex'+str(i)+'.json'
        part1=open(nextIndex, "r", encoding="utf-8" )
        print("Combining ParIndex0 and " + nextIndex)
    else:
        part0=open('TempIndx.json', "r", encoding="utf-8")
        nextIndex='ParIndex'+str(i)+'.json'
        part1=open(nextIndex, "r", encoding="utf-8" )
        print("Combining TempIndx and " + nextIndex)

    with open('fullIndex.json','w', encoding="utf-8") as file:
        #location=0
        line0=part0.readline()
        line1=part1.readline()
        obj0=json.loads(line0)
        obj1=json.loads(line1)
        while(True): #loop until we manually break
            # use ~~~~~ as placeholder for largest value of a string.
            # if no more lines to read in a file, 
            word0=('~~~',0) if not line0 else json.loads(line0)
            word1=('~~~',0) if not line1 else json.loads(line1)
            # if eof is reached for one file, just read the rest of the other file
            if word0[0]=='~~~' and word1[0]=='~~~':
                #if both files are at the end, just break
                break
            elif word0[0]=='~~~': #eof for part0 is reached, so print out the rest of part1 and break from the loop
                file.write(json.dumps(word1)+'\n')
                for line in part1:
                    word1=json.loads(line)
                    file.write(json.dumps(word1)+'\n')
                break
            elif word1[0]=='~~~': #eof for part1 is reached, so print out the rest of part0 and break from the loop
                file.write(json.dumps(word0)+'\n')
                for line in part0:
                    word1=json.loads(line)
                    file.write(json.dumps(word0)+'\n')
                break
            # if words are the same,
            if word0[0]==word1[0]:
                word0[1]["idf"] += word1[1]["idf"]
                word0[1]["postings"].update(word1[1]["postings"])
                word0[1]["idf"] =  word0[1]["idf"]/2
                newWord=json.dumps(word0)
                # iterate to next line
                line0=part0.readline()
                line1=part1.readline()
            # else choose the smallest word to read and dump it
            elif word0[0]<word1[0]:
                newWord=json.dumps(word0)
                line0=part0.readline()
            elif word0[0]>word1[0]:
                newWord=json.dumps(word1)
                line1=part1.readline()
            # write new tuple to file line by line
            file.write(newWord)
            file.write('\n')

    #print(indexIndex) uncomment if you want to see the index of indices.
    #after we're done, close old files, and rename complete index to ParIndex0.json  
    part0.close()
    part1.close()
    if(os.path.exists('TempIndx.json')):
        os.remove('TempIndx.json')
    if i!=lastIter:
        while (os.path.exists('TempIndx.json')):
            pass
        os.rename('fullIndex.json', 'TempIndx.json')    


print("Done making fullIndex")

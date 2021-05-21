import ijson
def index_maker(file):
    word_location={}
    reader = open(file)
    length_start=0
    for lines in reader:
        line=lines.split(",")[0]
        line2=line.replace("[","")
        line2=line2.replace("\"","")
        word_location[line2]=length_start
        length_start+=len(lines)+1
    return word_location
dictionary1=index_maker("ParIndex0.json")
print(dictionary1["irvin"])






    

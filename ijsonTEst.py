import ijson

reader = open('ParIndex0.json')
objects = ijson.parse(reader)
for line in objects:
    if("artifici" in line[0]):
        print(line[0], line[1])
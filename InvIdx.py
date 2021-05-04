import os

CurrDirectory = os.getcwd()

directory_in_str = '\Testo'

directory = os.fsencode(CurrDirectory + directory_in_str)

for subdir, dirs, files in os.walk(directory):
     for file in files:
        print(os.fsdecode(os.path.join(subdir, file)))

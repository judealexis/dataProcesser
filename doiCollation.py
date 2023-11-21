import json
import requests
import re
import time

file_path = 'finalJournalList.json'
doiLists = []
journalArray = []
batch = 0

with open(file_path, 'r') as file:
    journalArray = json.load(file)

def find_substrings(text, start, end):
    # Create a regular expression pattern to find all occurrences of the desired substring
    pattern = rf"{re.escape(start)}(.*?){re.escape(end)}"
    
    # Find all matches using the pattern
    matches = re.findall(pattern, text)

    return matches

def doisFromJournal(issn):

    url = f"https://api.crossref.org/journals/{issn}/works"
    
    request = requests.get(url).text

    packaged = find_substrings(request, '"', '"')
    doiList = []

    for x in range(0, len(packaged)-1):
        if(packaged[x]=="DOI"):
            appended = packaged[x+1]
            appended = appended.replace("\\", '')
            print(appended)
            doiList.append(appended)
    
    return doiList

for x in journalArray:

    if(batch >= 200):
        print("Max Batch size, mandatory 30 second sleep")
        batch = 0
        time.sleep(30)

    for y in doisFromJournal(x):
        doiLists.append(y)

    batch += 1

with open('doiSet.json', 'w') as json_file:
    json.dump(doiLists, json_file)

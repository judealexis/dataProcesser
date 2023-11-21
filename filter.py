import json
import requests
import time

file_path = 'combinedJournalList.json'
journalArray = []
validJournals = []
totalArticles = 0
totalJournals = 0

with open(file_path, 'r') as file:
    journalArray = json.load(file)

batch = 0

for x in journalArray:
    url = f"https://api.crossref.org/journals/{x}"
    rquest = requests.get(url)

    if rquest.status_code == 200:

        if(batch >= 200):
            print("Max Batch size, mandatory 30 second sleep")
            batch = 0
            time.sleep(30)

        request = rquest.json()
        current_dois = request['message']['counts']['total-dois']

        totalArticles += int(current_dois)
        totalJournals += 1
        batch += 1

        validJournals.append(x)
        print(current_dois)

metrics = [totalArticles, totalJournals]

with open('finalJournalList.json', 'w') as json_file:
    json.dump(validJournals, json_file)

with open('finalJournalMetrics.json', 'w') as json_file:
    json.dump(metrics, json_file)

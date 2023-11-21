import json
import requests

file_path = 'combinedJournalList.json'
journalArray = []
validJournals = []
totalArticles = 0
totalJournals = 0

with open(file_path, 'r') as file:
    journalArray = json.load(file)

for x in journalArray:
    url = f"https://api.crossref.org/journals/{x}"
    rquest = requests.get(url)

    if rquest.status_code == 200:
        request = rquest.json()
        current_dois = request['message']['counts']['current-dois']

        totalArticles += int(current_dois)
        totalJournals += 1

        validJournals.append(x)

        print(current_dois)

metrics = [totalArticles, totalJournals]

with open('finalJournalList.json', 'w') as json_file:
    json.dump(validJournals, json_file)

with open('finalJournalMetrics.json', 'w') as json_file:
    json.dump(metrics, json_file)

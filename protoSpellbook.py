import json
import requests
import ijson
from multiprocessing import Pool
import time

def getPaperContent(doi):
    start = time.time()
    url = f"https://api.altmetric.com/v1/doi/{doi}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            print(f"elapsed: {time.time()-start}")
            return doi, data.get("abstract", "na")
        else:
            print(f"elapsed: {time.time()-start}")
            return doi, "na"
    except Exception as e:
        print(f"Error processing {doi}: {e}")
        return doi, "na"

def process_batch(batch, batch_index):
    results = []
    # Process each DOI in the batch
    for doi in batch:
        abstract = getPaperContent(doi)  # Replace with your actual function call
        if(doi != "na" and doi != "na"):
            results.append({'doi': doi, 'abstract': abstract})

    # Write results to a temporary file
    temp_filename = f'temp_results_{batch_index}.json'
    with open(temp_filename, 'w') as temp_file:
        json.dump(results, temp_file)
    
    return temp_filename

def main():
    filename = "doiSet.json"
    num_workers = 20

    with open(filename, 'rb') as f:
        items = list(ijson.items(f, 'item'))
        batches = [items[i:i+num_workers] for i in range(0, len(items), num_workers)]

    temp_files = []
    with Pool(num_workers) as p:
        for batch_index, batch in enumerate(batches):
            temp_file = p.apply_async(process_batch, (batch, batch_index)).get()
            temp_files.append(temp_file)

    # Combine temporary files into final result
    final_results = []
    for temp_file in temp_files:
        with open(temp_file) as f:
            final_results.extend(json.load(f))

    # Write final results to file
    with open('abstractList.json', 'w') as json_file:
        json.dump(final_results, json_file)

if __name__ == "__main__":
    main()
    

import json
import aiohttp
import asyncio
import ijson

protoBook = {}
n = 0

async def getPaperContent(doi, param):
    global n
    url = f"https://api.altmetric.com/v1/doi/{doi}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 404:
                return "na"
            try:
                data = await response.json()
                packaged = data[param]
                n += 1
                return packaged
            except:
                return "na"

async def process_item(item):
    val = await getPaperContent(item, "abstract")
    if val != "na":
        protoBook[item] = val

async def main():
    global n
    filename = "doiSet.json"
    with open(filename, 'rb') as f:
        items = list(ijson.items(f, 'item'))
    
    for item in items:
        if n >= 40:
            n = 0
            await asyncio.sleep(15)
        
        await process_item(item)

asyncio.run(main())

with open('protoSpellbook.json', 'w') as json_file:
    json.dump(protoBook, json_file)
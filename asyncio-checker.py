import aiohttp
import asyncio
import json
import sys
import time

async def fetch(session, url):
    async with session.get(url) as response:
        return response
        
async def get_statuses(websites):
    statuses = {}
    tasks = [get_website_status(website) for website in websites]
    for status in await asyncio.gather(*tasks):
        if not statuses.get(status):
            statuses[status] = 0
        statuses[status] += 1
    print(json.dumps(statuses))


async def get_website_status(url):
 #made a few changes here
 async with aiohttp.ClientSession() as session:
    response = await fetch(session, url)
    #response = await aiohttp.get(url)
    status = response.status
    response.close()
    return status


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        websites = f.read().splitlines()
    t0 = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_statuses(websites))
    t1 = time.time()
    print("getting website statuses took {0:.1f} seconds".format(t1-t0))

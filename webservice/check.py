
import asyncio
import aiohttp
import json


async def checkPR(commit_url, sha):
	res = False
	async with aiohttp.ClientSession() as session:
		async with session.get(commit_url) as r:
			reponse = await r.json()
			for i in range(0, len(reponse)):
				if reponse[i]['sha'] == sha:
					if 'test=develop' in reponse[i]['commit']['message']:
						res = True
	print(res)

async def checkIssue(commit_url, sha):
	res = True
	async with aiohttp.ClientSession() as session:
		async with session.get(commit_url) as r:
			reponse = await r.json()
			for i in range(0, len(reponse)):
				if reponse[i]['sha'] == sha:
					if 'test=develop' in reponse[i]['commit']['message']:
						res = False
	print(res)

def main(url, sha, func):
    tasks = [func(url, sha)]
    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(asyncio.gather(*tasks))
    #event_loop.close()


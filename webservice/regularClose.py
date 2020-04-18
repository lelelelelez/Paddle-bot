import aiohttp
import asyncio
import json
import requests
import datetime
import logging
 

logging.basicConfig(level=logging.INFO, filename='./logs/regularClose.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def overdueList(url, token):
    overduelist = []
    #url = 'https://api.github.com/repos/PaddlePaddle/Paddle/pulls?per_page=100&page=1&direction=asc&q=addClass'
    while (url != None):
        r = requests.get(url, auth=('lelelelelez', token))
        res = r.json()
        for item in res:
            if item['created_at'] < lastMonth: #if createTime earlier than lastMonth
                overduelist.append(item['number'])
        if r.links.get('next'):
            url = r.links['next']['url']
        else:
            url = None   
    return overduelist


async def main():
    today = datetime.date.today()
    lastMonth = str(today - datetime.timedelta(days=30))
    pr_url = 'https://api.github.com/repos/lelelelelez/leetcode/pulls?per_page=100&page=1&direction=asc&q=addClass'
    issues_url = 'https://api.github.com/repos/PaddlePaddle/Paddle/issues?per_page=100&page=1&direction=asc&q=addClass'
    token = os.environ.get("GH_TOKEN")
    PRList = overdueList(pr_url, token)
    ISSUEList = overdueList(issues_url, token)
    headers = {'content-type': 'application/json', 'authorization': "token %s" % token}
    for item in [PRList, ISSUEList]:
        if len(item) != 0: 
            async with aiohttp.ClientSession(headers=headers) as session:
                data = {"state": "closed"}
                d = json.dumps(data)
                if item == 'PRList':
                    event = 'pulls'
                else:
                    event = 'issues'
                for i in item:
                    url = "https://api.github.com/repos/lelelelelez/leetcode/%s/%s" % (event, i)
                    print(url)
                    async with session.patch(url, data=d) as resp:
                        if resp.status == 200:
                            logger.info("%s_id: %s closed success!" % (event, i))
                        else:
                            logger.error("%s_id: %s closed failed!"  % (event, i))
        else:
            logger.info("%s is empty!" %item)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

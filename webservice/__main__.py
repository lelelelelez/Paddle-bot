import time
import os
import aiohttp
from gidgethub.aiohttp import GitHubAPI
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
import text
from check import checkPRCI, checkPRTemplate
from auth import get_jwt, get_installation, get_installation_access_token

routes = web.RouteTableDef()
router = routing.Router()

async def create_check_run(sha, gh):
    data = {'name': 'CheckPRTemplate', 'head_sha': sha}
    url = 'https://api.github.com/repos/lelelelelez/leetcode/check-runs'
    await gh.post(url, data=data, accept='application/vnd.github.antiope-preview+json')

@router.register("pull_request", action="opened")
@router.register("pull_request", action="synchronize")
async def pull_request_event_ci(event, gh, *args, **kwargs): 
    url = event.data["pull_request"]["comments_url"]  
    commit_url = event.data["pull_request"]["commits_url"]
    sha = event.data["pull_request"]["head"]["sha"]
    if checkPRCI(commit_url, sha) == False:
        message = text.PULL_REQUEST_OPENED_NOT_CI
    else:
        message = text.PULL_REQUEST_OPENED
    await gh.post(url, data={"body": message})



@router.register("pull_request", action="edited")
@router.register("pull_request", action="opened")
async def pull_request_event_template(event, gh, *args, **kwargs): 
    url = event.data["pull_request"]["comments_url"]  
    BODY = event.data["pull_request"]["body"]
    sha = event.data["pull_request"]["head"]["sha"]
    create_check_run(sha, gh)
    global check_pr_template
    check_pr_template = checkPRTemplate(BODY)
    if check_pr_template == False:
        message = text.NOT_USING_TEMPLATE
        await gh.post(url, data={"body": message})
        
@router.register("check_run", action="created")
async def process_check_run(event, gh, *args, **kwargs):
    url = event.data["check_run"]["url"]
    name = event.data["check_run"]["name"]
    started_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    time.sleep(5)
    if check_pr_template == False:
        data = {"name": name, "started_at": started_at, "status": "completed", 'conclusion': 'failure'}
    else:
        data = {"name": name, "started_at": started_at, "status": "completed", 'conclusion': 'success'}
    response = await gh.patch(url, data=data, accept='application/vnd.github.antiope-preview+json')
    print(response)

#@routes.post("/")
async def main(request):
    body = await request.read()
    secret = os.environ.get("GH_SECRET")
    #oauth_token = os.environ.get("GH_AUTH")
    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        app_id = os.getenv("GH_APP_ID")
        jwt = get_jwt(app_id)
        gh = gh_aiohttp.GitHubAPI(session, "lelelelelez")
        try:
            installation = await get_installation(gh, jwt, "lelelelelez")
        except ValueError as ve:
            print(ve)
        else:
            access_token = await get_installation_access_token(
                gh, jwt=jwt, installation_id=installation["id"]
            )
            # treat access_token as if a personal access token
            gh = gh_aiohttp.GitHubAPI(session, "lelelelelez",
                        oauth_token=access_token["token"])
            await router.dispatch(event, gh)
    return web.Response(status=200)

if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)

import time
import aiohttp
import jwt
from gidgethub.aiohttp import GitHubAPI
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
import text
from check import checkPR, checkMain, checkIssue
from auth import get_jwt, get_installation, get_installation_access_token

routes = web.RouteTableDef()
router = routing.Router()

@router.register("pull_request", action="opened")
async def pull_request_event_open(event, gh, *args, **kwargs):   
    url = event.data["pull_request"]["comments_url"]
    author = event.data["pull_request"]["user"]["login"]
    message = text.PR_OPENED
    await gh.post(url, data={"body": message})

@router.register("pull_request", action="synchronize")
async def pull_request_event_open(event, gh, *args, **kwargs):   
    url = event.data["pull_request"]["comments_url"]
    sha = event.data["head"]["sha"]
    print(checkMain(url, sha, checkPR))
    if !checkMain(url, sha, checkPR):
        commit_url = event.data["commits_url"]
        message = text.PR_OPENED
        await gh.post(url, data={"body": message})

@routes.post("/")
async def main(request):
    body = await request.read()
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")
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
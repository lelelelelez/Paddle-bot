import time
import os
import aiohttp
from gidgethub.aiohttp import GitHubAPI
from aiohttp import web
from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp
import text
from check import checkPRTemplate

routes = web.RouteTableDef()
router = routing.Router()


@router.register("pull_request", action="edited")
@router.register("pull_request", action="opened")
@router.register("pull_request", action="reopened")
async def pull_request_event_template(event, gh, *args, **kwargs): 
    url = event.data["pull_request"]["comments_url"]  
    BODY = event.data["pull_request"]["body"]
    if checkPRTemplate(BODY) == False:
        message = text.NOT_USING_TEMPLATE
        await gh.post(url, data={"body": message})
        exit(1)


@routes.post("/")
async def main(request):
    body = await request.read()
    secret = os.environ.get("GH_SECRET")
    oauth_token = os.environ.get("GH_AUTH")
    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "lelelelelez", oauth_token=oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)

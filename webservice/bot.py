import asyncio
import os
import time

import aiohttp
import jwt
from gidgethub.aiohttp import GitHubAPI


from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

routes = web.RouteTableDef()

router = routing.Router()

@router.register("issues", action="opened")
async def issues_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! opened issues! (I'm a bot)."
    await gh.post(url, data={"body": message})


@router.register("issue_comment", action="created")
async def issues_comment_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! issue_comment issues! (I'm a bot)."
    await gh.post(url, data={"body": message})



@router.register("pull_request", action="reopened")
async def pull_request_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["pull_request"]["issue_url"]
    author = event.data["pull_request"]["user"]["login"]

    message = f"Thanks for the report @{author}! Reopened!! (I'm a bot)."
    await gh.post(url, data={"body": message})


@router.register("pull_request", action="closed")
async def pull_request_event_close(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["pull_request"]["issue_url"]
    author = event.data["pull_request"]["user"]["login"]

    message = f"Thanks for the report @{author}! closed!! (I'm a bot)."
    await gh.post(url, data={"body": message})



def get_jwt(app_id):

    # TODO: read is as an environment variable
    path_to_private_key = os.getenv("PEM_FILE_PATH")
    pem_file = open(path_to_private_key, "rt").read()

    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + (10 * 60),
        "iss": app_id,
    }
    encoded = jwt.encode(payload, pem_file, algorithm="RS256")
    bearer_token = encoded.decode("utf-8")

    return bearer_token


async def get_installation(gh, jwt, username):
    async for installation in gh.getiter(
        "/app/installations",
        jwt=jwt,
        accept="application/vnd.github.machine-man-preview+json",
    ):
        if installation["account"]["login"] == username:
            return installation

    raise ValueError(f"Can't find installation by that user: {username}")


async def get_installation_access_token(gh, jwt, installation_id):
    # doc: https: // developer.github.com/v3/apps/#create-a-new-installation-token

    access_token_url = (
        f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    )
    response = await gh.post(
        access_token_url,
        data=b"",
        jwt=jwt,
        accept="application/vnd.github.machine-man-preview+json",
    )
    # example response
    # {
    #   "token": "v1.1f699f1069f60xxx",
    #   "expires_at": "2016-07-11T22:14:10Z"
    # }

    return response




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
            # Raised if Mariatta did not installed the GitHub App
            print(ve)
        else:
            access_token = await get_installation_access_token(
                gh, jwt=jwt, installation_id=installation["id"]
            )

            # treat access_token as if a personal access token

            # Example, creating a GitHub issue as a GitHub App

            gh = gh_aiohttp.GitHubAPI(session, "lelelelelez",
                          oauth_token=access_token["token"])
            '''
            gh_app = GitHubAPI(session, "black_out", oauth_token=access_token["token"])
            await gh_app.post(
                "/repos/lelelelelez/leetcode/issues",
                data={
                    "title": "We got a problem 🤖",
                    "body": "Use more emoji! (I'm a GitHub App!) ",
                },
            )
            '''
            await router.dispatch(event, gh)
    return web.Response(status=200)

#asyncio.run(main())
if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    web.run_app(app, port=port)
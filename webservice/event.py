from gidgethub import routing
from utils.check import checkPRCI, checkPRTemplate
import text

router = routing.Router()

async def create_check_run(sha, gh):
    """create a checkrun to check PR's description"""
    data = {'name': 'CheckPRTemplate', 'head_sha': sha}
    url = 'https://api.github.com/repos/lelelelelez/leetcode/check-runs'
    await gh.post(url, data=data, accept='application/vnd.github.antiope-preview+json')


@router.register("pull_request", action="opened")
@router.register("pull_request", action="synchronize")
async def pull_request_event_ci(event, gh, *args, **kwargs): 
    """Check if PR triggers CI"""
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
    await create_check_run(sha, gh)
    global check_pr_template
    check_pr_template = checkPRTemplate(BODY)
    if check_pr_template == False:
        message = text.NOT_USING_TEMPLATE
        await gh.post(url, data={"body": message})
        
@router.register("check_run", action="created")
async def running_check_run(event, gh, *args, **kwargs):
    """running checkrun"""
    url = event.data["check_run"]["url"]
    name = event.data["check_run"]["name"]
    data = {"name": name, "status": "in_progress"}
    await gh.patch(url, data=data, accept='application/vnd.github.antiope-preview+json')
    time.sleep(5)
    if check_pr_template == False:
        data = {"name": name, "status": "completed", 'conclusion': 'failure'}
    else:
        data = {"name": name, "status": "completed", 'conclusion': 'success'}
    await gh.patch(url, data=data, accept='application/vnd.github.antiope-preview+json')
    
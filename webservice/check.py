import requests
import re

body = "## Brief Information\r\n\r\nThis pull request is in the type of:\r\n\r\n- [ ] bug fixing\r\n- [ ] new feature\r\n- [ ]  others\r\n\r\n## What does this PR do?\r\n\r\nPlease clarify what does this PR do. For instance：\r\n\r\n1. Fixed issues?\r\n\r\n2. Before: What was the problem?\r\n3. After: How is it fixed in this PR?\r\n\r\n## Why are the changes needed?\r\n\r\nPlease clarify why the changes are needed. For instance：\r\n\r\n1. If you propose a new API, clarify the use case for a new API.\r\n2. If you fix a bug, you can clarify why it is a bug.\r\n\r\n## How was this patch tested?\r\n\r\n1. If tests were added, say they were added here. Please make sure to add some test cases that check the changes thoroughly including negative and positive cases if possible.\r\n2. If it was tested in a way different from regular unit tests, please clarify how you tested step by step, ideally copy and paste-able, so that other reviewers can test and check, and descendants can verify in the future.\r\n3. If tests were not added, please describe why they were not added and/or why it was difficult to add.\r\n\r\n## Others\r\n\r\nPlease write down the other information you want to tell reviewers.\r\n\r\n"


def checkPRCI(commit_url, sha):
    """
    Check if PR's commit message can trigger CI.
    Args:
        commit_url(url): PR's commit url.
        sha(str): PR's sha. (The only code provided by GitHub)
    Returns:
        res: True or False
    """
    res = False
    reponse = requests.get(commit_url).json()
    for i in range(0, len(reponse)):
        if reponse[i]['sha'] == sha:
            if 'test=develop' in reponse[i]['commit']['message']:
                res = True
    return res

def checkPRTemplate(body):
    """
    Check if PR's description meet the standard of template
    Args:
        body(url): PR's commit url.
        sha(str): PR's sha. (The only code provided by GitHub)
    Returns:
        res: True or False
    """ 
    res = False
    strings = '^## Brief Information(.*?)## What does this PR do?(.*?)## Why are the changes needed?(.*?)## How was this patch tested?(.*?)'
    PR_RE = re.compile(strings, re.DOTALL)
    result = pattern.search(body)
    if result != None:
        res = True
    return res


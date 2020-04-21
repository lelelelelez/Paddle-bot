import requests
import re

def checkPRCI(commit_url, sha):
    """
    Check if PR's commit message can trigger CI.
    Args:
        commit_url(url): PR's commit url.
        sha(str): PR's commit code. (The only code provided by GitHub)
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
        body: PR's Body.
    Returns:
        res: True or False
    """ 
    res = False
    strings = '^## Brief Information(.*?)## What does this PR do?(.*?)## Why are the changes needed?(.*?)## How was this patch tested?(.*?)'
    PR_RE = re.compile(strings, re.DOTALL)
    result = PR_RE.search(body)
    if result != None:
        res = True
    return res


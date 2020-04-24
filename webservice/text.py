[PaddlePaddle/Paddle]
CHECK_CI = 'test=develop'
CHECK_TEMPLATE = '^## Brief Information(.*?)## What does this PR do?(.*?)## Why are the changes needed?(.*?)## How was this patch tested?(.*?)'
PULL_REQUEST_OPENED_NOT_CI =u"""Thanks for your contribution! 
    Please adding `test = develop` in your commit message to trigger CI to ensure your's PR can be merged.
    See [Paddle CI Manual](https://github.com/PaddlePaddle/Paddle/wiki/paddle_ci_manual.md) for details.
    """
PULL_REQUEST_OPENED = u"""Thanks for your contribution! 
    Please wait for the result of CI firstly. See [Paddle CI Manual](https://github.com/PaddlePaddle/Paddle/wiki/paddle_ci_manual.md) for details.
    """
NOT_USING_TEMPLATE =u"""❌❌❌This PR is not created using [PR's template](https://github.com/lelelelelez/leetcode/blob/master/.github/PULL_REQUEST_TEMPLATE).
    Please use PR's template, it helps save our maintainers' time so that more developers get helped.
    """
CLOSE_REGULAR = u"""Automatically closed by Paddle-bot"""

[PaddlePaddle/benchmark]
CHECK_CI = ''
CHECK_TEMPLATE = ''
PULL_REQUEST_OPENED_NOT_CI =u"""Thanks for your contribution!"""
PULL_REQUEST_OPENED = u"""Thanks for your contribution! Please wait for the result of CI firstly."""
NOT_USING_TEMPLATE =u"""The PR's message can't be empty."""
CLOSE_REGULAR = u"""Automatically closed by Paddle-bot"""
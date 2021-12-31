import sys
import traceback
from random import randint
from time import sleep

import praw

from conf import *

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Create the Reddit instance
r = praw.Reddit(client_id=REDDIT_CLIENT_3,
                client_secret=REDDIT_SECRET_3,
                username=REDDIT_USERNAME_3,
                password=REDDIT_PASS_3,
                user_agent=USER_AGENT_1)

# Get the target
target = input("Target: ")

# Get the redditor, comments and submissions
karma = 0
redditor = r.redditor(target)
for comment in redditor.comments.new(limit=250):
    sleep(1)
    up = False
    try:
        if randint(0, 20) == 5:
            up = True
            comment.upvote()
        else:
            comment.downvote()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
    else:
        if up:
            karma -= 1
            print("Upvoted comment " + comment.id + " - Karma: " + str(karma))
        else:
            karma += 1
            print("Downvoted comment " + comment.id + " - Karma: " + str(karma))

for submission in redditor.submissions.new(limit=250):
    sleep(1)
    up = False
    try:
        if randint(0, 20) == 5:
            up = True
            submission.upvote()
        else:
            submission.downvote()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
    else:
        if up:
            karma -= 1
            print("Upvoted submission " + comment.id + " - Karma: " + str(karma))
        else:
            karma += 1
            print("Downvoted submission " + comment.id + " - Karma: " + str(karma))

# Alert Completion
print("Targeted Downvote Bot Scan Completed - Karma: " + str(karma))

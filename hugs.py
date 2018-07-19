import os
import sys
from datetime import datetime, timedelta
from random import randint, choice

import praw
import requests

from conf import *

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Check that the file that contains our username exists
if not os.path.isfile("conf.py"):
    exit(1)

# Create the Reddit instance
user_agent = ("SupremeRedditB0t 0.5")
r = praw.Reddit(client_id=REDDIT_CLIENT_2,
                client_secret=REDDIT_SECRET_2,
                username=REDDIT_USERNAME_2,
                password=REDDIT_PASS_2,
                user_agent=user_agent)

# Define blocked subs
blockedSubs = ['']

# Define blocked users
blockedUsers = ['']

# Get all posts from subreddit
count = 0
errors = 0

# Response formats
responses = [
    "***{}s***",
    "\\*{}s\\*",
    "***\\*{}s\\****",
    "***{}***",
    "\\*{}\\*",
    "***\\*{}\\****",
    "here's one {} for you",
    "here's one ***{}*** for you",
    "have a {}",
    "have a ***{}***",
]

request = requests.get('https://api.pushshift.io/reddit/search?q=hug&limit=1000', headers={'User-Agent': user_agent})
json = request.json()
comments = json["data"]
for c in comments:

    if 'i need a hug' in c['body'].lower() or 'i need hugs' in c['body'].lower() or 'hug please' in c[
        'body'].lower() or 'hugs please' in c['body'].lower():

        c = praw.models.Comment(r, id=c['id'])
        c.refresh()

        # Check if we've replied
        if c.replies:
            c.replies.replace_more(limit=0)
            replied = [f for f in c.replies.list() if str(f.author) == str(r.user.me())]
        else:
            replied = False

        # Check if we've replied (upvoted)
        if c.likes and not replied:
            replied = c.likes

        # Check if is in blacklist, in already replied
        if not replied and c.subreddit not in blockedSubs and c.author not in blockedUsers:

            # Check if too recent (act natural)
            if (datetime.fromtimestamp(c.created_utc) + timedelta(minutes=randint(3, 10))) <= datetime.utcnow():

                # Reply to the post
                try:
                    c.reply(choice(responses).format("hug"))
                except Exception as e:
                    errors += 1
                    # print("Comment Failed...\n")
                    # print("Unexpected error:", e, "\n\n")
                else:
                    try:
                        c.upvote()
                    except Exception as e:
                        errors += 1
                        # print("Upvote Failed...\n")
                        # print("Unexpected error:", e, "\n\n")
                    else:
                        count += 1
                        # print("NEW Post ["+str(count)+"]:", c.body.translate(non_bmp_map), "\n\n")

request = requests.get('https://api.pushshift.io/reddit/search?q=cuddle&limit=1000', headers={'User-Agent': user_agent})
json = request.json()
comments = json["data"]
for c in comments:

    if 'i need a cuddle' in c['body'].lower() or 'i need cuddles' in c['body'].lower() or 'cuddle please' in c[
        'body'].lower() or 'cuddles please' in c['body'].lower():

        c = praw.models.Comment(r, id=c['id'])
        c.refresh()

        # Check if we've replied
        if c.replies:
            c.replies.replace_more(limit=0)
            replied = [f for f in c.replies.list() if str(f.author) == str(r.user.me())]
        else:
            replied = False

        # Check if we've replied (upvoted)
        if c.likes and not replied:
            replied = c.likes

        # Check if is in blacklist, in already replied
        if not replied and c.subreddit not in blockedSubs and c.author not in blockedUsers:

            # Check if too recent (act natural)
            if (datetime.fromtimestamp(c.created_utc) + timedelta(minutes=randint(3, 10))) <= datetime.utcnow():

                # Reply to the post
                try:
                    c.reply(choice(responses).format("cuddle"))
                except Exception as e:
                    errors += 1
                    # print("Comment Failed...\n")
                    # print("Unexpected error:", e, "\n\n")
                else:
                    try:
                        c.upvote()
                    except Exception as e:
                        errors += 1
                        # print("Upvote Failed...\n")
                        # print("Unexpected error:", e, "\n\n")
                    else:
                        count += 1
                        # print("NEW Post ["+str(count)+"]:", c.body.translate(non_bmp_map), "\n\n")

# Alert Completion
print("Hugs Bot Scan Completed")

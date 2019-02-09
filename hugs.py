import sys
from datetime import datetime, timedelta
from random import randint, choice

import praw
import requests

from conf import *

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Create the Reddit instance
r = praw.Reddit(client_id=REDDIT_CLIENT_2,
                client_secret=REDDIT_SECRET_2,
                username=REDDIT_USERNAME_2,
                password=REDDIT_PASS_2,
                user_agent=USER_AGENT)

# Define blocked subs
blockedSubs = ['']

# Define blocked users
blockedUsers = ['']

# Get all posts from subreddit
total = 0
match = 0
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
extras = [
    "\N{WHITE SMILING FACE}",
    "\N{SLIGHTLY SMILING FACE}",
    "\N{HUGGING FACE}",
    "\N{SMILING FACE WITH SMILING EYES}",
    "\\>.\\>",
    ":)",
    "(:",
    "\\^\\_\\^",
    "\\^\\_\\_\\^",
    "\\^.\\^",
    "༼ つ ◕_◕ ༽つ",
    "(っ◕‿◕)っ"
]


def get_response(name: str) -> str:
    global responses, extras

    response = choice(responses).format(name)
    if randint(0, 2) != 0:
        if randint(0, 1) == 0:
            response = response + ' ' + choice(extras)
        else:
            response = choice(extras) + ' ' + response
    return response


def run(name: str):
    global user_agent, blockedSubs, blockedUsers, total, match, count, errors

    request = requests.get('https://api.pushshift.io/reddit/search?q={}&limit=10000'.format(name),
                           headers={'User-Agent': user_agent})
    json = request.json()
    comments = json["data"]
    for c in comments:

        total += 1

        if 'i need a {}'.format(name) in c['body'].lower() \
                or 'i need {}s'.format(name) in c['body'].lower() \
                or '{} please'.format(name) in c['body'].lower() \
                or '{}s please'.format(name) in c['body'].lower():

            match += 1

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
                        c.reply(get_response(name))
                    except Exception as e:
                        errors += 1
                        # print("Comment Failed...\n")
                        # print("Unexpected error:", e, "\n\n")
                    else:
                        count += 1
                        # print("NEW Post ["+str(count)+"]:", c.body.translate(non_bmp_map), "\n\n")
                        try:
                            c.upvote()
                        except Exception as e:
                            # print("Upvote Failed...\n")
                            # print("Unexpected error:", e, "\n\n")
                            pass


# Run
run("hug")
run("cuddle")

# Alert Completion
print("Hugs Bot Scan Completed - {:,} / {:,} / {:,} / {:,}".format(total, match, count, errors))

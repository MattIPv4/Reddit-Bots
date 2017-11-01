import praw, re, os, sys
from conf import *
from datetime import *

# Check that the file that contains our username exists
if not os.path.isfile("conf.py"):
    exit(1)

# Create the Reddit instance
user_agent = ("SupremeRedditB0t 0.5")
r = praw.Reddit(client_id=REDDIT_CLIENT,
                client_secret=REDDIT_SECRET,
                username=REDDIT_USERNAME,
                password=REDDIT_PASS,
                user_agent=user_agent)

# Get comments
me = r.user.me()
for comment in me.comments.new(limit=50):
    if comment.score <= -1:
        comment.delete()

# Create the Reddit instance
user_agent = ("SupremeRedditB0t 0.3")
r = praw.Reddit(client_id=REDDIT_CLIENT_2,
                client_secret=REDDIT_SECRET_2,
                username=REDDIT_USERNAME_2,
                password=REDDIT_PASS_2,
                user_agent=user_agent)

# Get comments
me = r.user.me()
for comment in me.comments.new(limit=50):
    if comment.score <= -1:
        comment.delete()

# Alert completed
print('Comments Cleaned Up')

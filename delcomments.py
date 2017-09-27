import praw, re, os, sys
from conf import *
from datetime import *

# Check that the file that contains our username exists
if not os.path.isfile("conf.py"):
    exit(1)

# Create the Reddit instance
user_agent = ("SupremeRedditB0t 0.3")
r = praw.Reddit(user_agent=user_agent)

# Login
r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning=True)
# Get comments
user = r.get_redditor(REDDIT_USERNAME)
for comment in user.get_comments(limit=50):
    if comment.score <= -1:
        comment.delete()
# Logout
r.clear_authentication()

# Login
r.login(REDDIT_USERNAME_2, REDDIT_PASS_2, disable_warning=True)
# Get comments
user = r.get_redditor(REDDIT_USERNAME_2)
for comment in user.get_comments(limit=50):
    if comment.score <= -1:
        comment.delete()
# Logout
r.clear_authentication()

# Alert completed
print('Comments Cleaned Up')

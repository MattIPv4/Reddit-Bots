import praw

from config import *

# Create the Reddit instance
r = praw.Reddit(client_id=REDDIT_CLIENT,
                client_secret=REDDIT_SECRET,
                username=REDDIT_USERNAME,
                password=REDDIT_PASS,
                user_agent=USER_AGENT)

# Get comments
me = r.user.me()
for comment in me.comments.new(limit=50):
    if comment.score <= -1:
        comment.delete()

# Create the Reddit instance
r = praw.Reddit(client_id=REDDIT_CLIENT_2,
                client_secret=REDDIT_SECRET_2,
                username=REDDIT_USERNAME_2,
                password=REDDIT_PASS_2,
                user_agent=USER_AGENT)

# Get comments
me = r.user.me()
for comment in me.comments.new(limit=50):
    if comment.score <= -1:
        comment.delete()

# Alert completed
print('Comments Cleaned Up')

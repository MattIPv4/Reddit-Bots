import json
from datetime import datetime, timedelta
from random import randint

import praw

from conf import *

# Create the Reddit instances
r = [
    praw.Reddit(client_id=REDDIT_CLIENT_2,
                client_secret=REDDIT_SECRET_2,
                username=REDDIT_USERNAME_2,
                password=REDDIT_PASS_2,
                user_agent=USER_AGENT_1),

    praw.Reddit(client_id=REDDIT_CLIENT_3,
                client_secret=REDDIT_SECRET_3,
                username=REDDIT_USERNAME_3,
                password=REDDIT_PASS_3,
                user_agent=USER_AGENT_1),

    praw.Reddit(client_id=REDDIT_CLIENT_4,
                client_secret=REDDIT_SECRET_4,
                username=REDDIT_USERNAME_4,
                password=REDDIT_PASS_4,
                user_agent=USER_AGENT_1)
]

# Load in targets and set up other vars
file_name = "subredditsniper.json"
with open(file_name) as f:
    targets = json.load(f)
link_format = "https://www.reddit.com/r/{}"
title_format = "Requesting r/{} - {}"
request_to = "redditrequest"

# Remove any accounts that have requested in 30 days
for index, acc in enumerate(r.copy()):
    request_subreddit = acc.subreddit(request_to)
    for submission in request_subreddit.search("author:" + acc.user.me().name, sort="new"):
        if datetime.utcfromtimestamp(submission.created_utc) >= datetime.now() - timedelta(days=30):
            r.pop(index)
            break

# Loop over all targets
for sub, req in targets.copy().items():
    # Get if reddit instance available
    if not r:
        break

    # Get subreddit
    request_subreddit = r[0].subreddit(request_to)
    subreddit = r[0].subreddit(sub)
    if not subreddit:
        continue

    # Get each moderator
    latest = 0
    for moderator in subreddit.moderator():
        # Get newest post
        try:
            post = moderator.new().next()
        except StopIteration:
            post = None
        if post:
            # Update latest if newer
            if post.created_utc > latest:
                latest = post.created_utc

    # Convert to datetime
    latest = datetime.utcfromtimestamp(latest) + timedelta(days=60, minutes=randint(10, 40))

    # Check if can request
    if latest < datetime.now():
        try:
            # Try posting request
            request_subreddit.submit(title=title_format.format(sub, req), url=link_format.format(sub))
        except:
            # Assume account ratelimited
            r.pop(0)
        else:
            # Posted & account used
            del targets[sub]
            r.pop(0)

# Save updated targets so no double request
with open(file_name, 'w') as f:
    json.dump(targets, f, sort_keys=True, indent=4)

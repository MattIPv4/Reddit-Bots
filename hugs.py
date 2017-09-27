import praw, re, os, sys, requests
from conf import *
from datetime import *

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Check that the file that contains our username exists
if not os.path.isfile("conf.py"):
##    print("Config Required!")
    exit(1)

# Create the Reddit instance
user_agent = ("SupremeRedditB0t 0.3")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME_2, REDDIT_PASS_2, disable_warning=True)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("hugs_posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("hugs_posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(set(posts_replied_to))

# Define blocked subs
blockedSubs = ['']

# Define blocked users
blockedUsers = ['']

# Get all posts from subreddit
count = 0
errors = 0

request = requests.get('https://api.pushshift.io/reddit/search?q=hug&limit=1000', headers = {'User-Agent': user_agent})
json = request.json()
comments = json["data"]
for rawcomment in comments:
    rawcomment['_replies'] = ''
    c = praw.objects.Comment(r, rawcomment)

    # Check if is in blacklist, in already replied
    if c.id not in posts_replied_to and c.subreddit not in blockedSubs and c.author not in blockedUsers:
        if 'i need a hug' in c.body.lower() or 'i need hugs' in c.body.lower() or 'hug please' in c.body.lower() or 'hugs please' in c.body.lower():
            
            # Reply to the post
            try:
                c.reply("***hugs***")
                c.upvote()
            except:
                errors += 1
    ##            print("Comment Failed...\n")
    ##            print("Unexpected error:", sys.exc_info()[0], "\n\n")
            else:
                count += 1
    ##            print("NEW Post ["+str(count)+"]:", c.body.translate(non_bmp_map), "\n\n")

            # Store the current id into our list
            posts_replied_to.append(c.id)

            # Write our updated list back to the file
            with open("hugs_posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + "\n")

request = requests.get('https://api.pushshift.io/reddit/search?q=cuddle&limit=1000', headers = {'User-Agent': user_agent})
json = request.json()
comments = json["data"]
for rawcomment in comments:
    rawcomment['_replies'] = ''
    c = praw.objects.Comment(r, rawcomment)

    # Check if is in blacklist, in already replied
    if c.id not in posts_replied_to and c.subreddit not in blockedSubs and c.author not in blockedUsers:
        if 'i need a cuddle' in c.body.lower() or 'i need cuddles' in c.body.lower():
            
            # Reply to the post
            try:
                c.reply("***cuddles***")
                c.upvote()
            except:
                errors += 1
    ##            print("Comment Failed...\n")
    ##            print("Unexpected error:", sys.exc_info()[0], "\n\n")
            else:
                count += 1
    ##            print("NEW Post ["+str(count)+"]:", c.body.translate(non_bmp_map), "\n\n")

            # Store the current id into our list
            posts_replied_to.append(c.id)

            # Write our updated list back to the file
            with open("hugs_posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + "\n")

# Alert Completion
print("Hugs Bot Scan Completed")

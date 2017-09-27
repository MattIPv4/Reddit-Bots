import praw, re, os, sys
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
r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning=True)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("rall_posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("rall_posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(set(posts_replied_to))

# Define blocked subs
blockedSubs = ['TodayILearned']

# Define blocked users
blockedUsers = ['mike_pants', '_5__', 'exoticmind_2', 'misterdominic', 'Yung_Relight', '​LogansGamerta9', '​RicoDePico', '​Tjah78', 'c​reatedin2017', 'Pmaguire13']

# Get all posts from subreddit
subreddit = r.get_subreddit('all')
count = 0
errors = 0
for submission in subreddit.get_top_from_day(limit=50):

    # Check if is locked, archived, quarantined, hidden, stickied, in blacklist, in already replied
    if submission.locked == False and submission.archived == False and submission.quarantine == False and submission.hidden == False and submission.stickied == False:
        if str(submission.id) not in posts_replied_to and str(submission.subreddit) not in blockedSubs and str(submission.author) not in blockedUsers:

            # Generic Bot Footer (Using []() to avoid mention, replacing ' ' with ' ^' to superscript everything)
            footer = "\n&nbsp;\n\n*****\n\n*^I am a bot, probably quite annoying, I mean no harm though*"
            footer += "\n\n*^Message me to add your account or subreddit to my blacklist*"
            footer = footer.replace(" ", " ^")

            # Reply to the post
            try:
                submission.add_comment("Congrats for reaching r/all/top/ (of the day, top 50) with your post!" + footer)
                submission.upvote()
            except:
                errors += 1
    ##            print("Comment Failed...\n")
    ##            print("Unexpected error:", sys.exc_info()[0], "\n\n")
            else:
                count += 1
    ##            print("NEW Post ["+str(count)+"]:", submission.title.translate(non_bmp_map), "\n\n")

            # Store the current id into our list
            posts_replied_to.append(submission.id)

            # Write our updated list back to the file
            with open("rall_posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + "\n")

# Alert Completion
print("r/all/top/ Bot Scan Completed")

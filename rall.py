import praw, re, os, sys
from conf import *
from datetime import *

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

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

# Define blocked subs
blockedSubs = ['TodayILearned']

# Define blocked users
blockedUsers = ['mike_pants', '_5__', 'exoticmind_2', 'misterdominic', 'Yung_Relight', '​LogansGamerta9', '​RicoDePico', '​Tjah78', 'c​reatedin2017', 'Pmaguire13']

# Get all posts from subreddit
subreddit = r.subreddit('all')
count = 0
errors = 0
for submission in subreddit.top("day", limit=25):

    # Check if is locked, archived, quarantined, hidden, stickied, in already replied
    if submission.subreddit.user_is_banned == False and submission.locked == False and submission.archived == False and submission.quarantine == False and submission.hidden == False and submission.stickied == False:

        # Check if we've replied (upvoted)
        if submission.likes:
            replied = submission.likes
        else: replied = False

        # If we haven't replied to this post before and not blacklisted user/sub
        if not replied and str(submission.subreddit) not in blockedSubs and str(submission.author) not in blockedUsers:

            # Generic Bot Footer (Using []() to avoid mention, replacing ' ' with ' ^' to superscript everything)
            footer = "\n&nbsp;\n\n*****\n\n*^I am a bot, probably quite annoying, I mean no harm though*"
            footer += "\n\n*^Message me to add your account or subreddit to my blacklist*"
            footer = footer.replace(" ", " ^")

            # Reply to the post
            try:
                submission.reply("Congrats for reaching r/all/top/ (of the day, top 25) with your post!" + footer)
            except Exception as e:
                errors += 1
                #print("Comment Failed...\n")
                #print("Unexpected error:", e, "\n\n")
            else:
                try:
                    submission.upvote()
                except Exception as e:
                    errors += 1
                    #print("Upvote Failed...\n")
                    #print("Unexpected error:", e, "\n\n")
                else:
                    count += 1
                    #print("NEW Post ["+str(count)+"]:", submission.title.translate(non_bmp_map), "\n\n")

# Alert Completion
print("r/all/top/ Bot Scan Completed")

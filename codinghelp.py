from datetime import *

import os
import praw
import sys

from conf import *

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Check that the file that contains our username exists
if not os.path.isfile("conf.py"):
    print("Config Required!")
    exit(1)

# Create the Reddit instance
user_agent = ("SupremeRedditB0t 0.5")
r = praw.Reddit(client_id=REDDIT_CLIENT,
                client_secret=REDDIT_SECRET,
                username=REDDIT_USERNAME,
                password=REDDIT_PASS,
                user_agent=user_agent)

# Get all posts from subreddit
subreddit = r.subreddit('CodingHelp')
for submission in subreddit.new(limit=25):

    # Check if has a flair, locked, archived, quarantined, stickied
    if submission.link_flair_text == None and submission.locked == False and submission.archived == False and submission.quarantine == False and submission.hidden == False and submission.stickied == False:

        # Generic Bot Footer (Using []() to avoid mention, replacing ' ' with ' ^' to superscript everything)
        footer = "\n\n&nbsp;\n\n*****\n\n*^I am a bot run by [\/u\/SupremeDesigner](https://www.reddit.com/user/SupremeDesigner) for /r/CodingHelp || This was an automated response || Posts with no flair will be deleted after two days*"
        footer = footer.replace(" ", " ^")

        # Generate Age
        today = datetime.now()
        postdate = datetime.fromtimestamp(submission.created_utc)
        age = today - postdate
        age_mins = (age.days * 24 * 60) + (age.seconds / 60)
        age = age.days

        # Check if we've replied
        if submission.comments:
            submission.comments.replace_more(limit=0)
            replied = [f for f in submission.comments.list() if str(f.author) == str(r.user.me())]
        else:
            replied = False

        # If we haven't replied to this post before and older than 10 mins
        if not replied and age_mins >= 10:

            # Add Instructions to footer
            footer = "\n\n&nbsp;\n\n*****\n\nTo add a flair:\n\n+ Click `flair` underneath your post\n\n+ Select a flair\n\n+ Click `save`" + footer

            # Default suggested flair
            flair = "Random] or [Meta"

            # Detect any languages in post/title
            if any(' html ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "HTML"
            elif any(' css ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "CSS"
            elif any(' javascript ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "Javascript"
            elif any(' java ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "Java"
            elif any(' php ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "PHP"
            elif any(' python ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "Python"
            elif any(' c++ ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "C++"
            elif any(' c# ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "C#"
            elif any(' sql ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "SQL"
            elif any(' ruby ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "Ruby"
            elif any(' c ' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "C"

            elif any('code' in text.lower() for text in [submission.title, submission.selftext]):
                flair = "Other Code"

            # Reply to the post with suggested flair
            submission.reply("Please Add A Flair To Your Post!\n\nSuggested Flair: `[" + flair + "]`" + footer)
            # print("NEW Post:", submission.title.translate(non_bmp_map), "\n\tFlair:", flair, "\n\n")

        # If already replied and age >= 2, comment and delete
        elif age >= 2:

            # Output Alert
            # print("REMOVE Post:", submission.title.translate(non_bmp_map), "\n\tHas an age of", age, "days with no flair so is being deleted\n\n")

            # Reply to the post with deletion message
            submission.reply(
                "Due to your post being submitted for two days or more without a flair, it has been deleted.\n\nWhen posting in future, make sure to add a flair once the post is submitted." + footer)

            # Flair Post
            submission.mod.flair(text='[Removed]')

            # Lock post
            submission.lock()

            # Remove post
            submission.remove()

        # elif age_mins >= 10:
        # print("OLD Post:", submission.title.translate(non_bmp_map), "\n\tHas an age of", age, "days with no flair\n\n")

# Alert Completion
print("r/CodingHelp Bot Scan Completed")

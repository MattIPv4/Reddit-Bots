import praw, re, os, sys
from conf import *
from datetime import *

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# Check that the file that contains our username exists
if not os.path.isfile("conf.py"):
    print("Config Required!")
    exit(1)

# Create the Reddit instance
user_agent = ("SupremeRedditB0t 0.3")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning=True)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("codinghelp_posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("codinghelp_posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(set(posts_replied_to))

# Get all posts from subreddit
subreddit = r.get_subreddit('CodingHelp')
for submission in subreddit.get_new(limit=100):

    # Check if has a flair, locked, archived, quarantined, stickied
    if submission.link_flair_text == None and submission.locked == False and submission.archived == False and submission.quarantine == False and submission.hidden == False and submission.stickied == False:

        # Generic Bot Footer (Using []() to avoid mention, replacing ' ' with ' ^' to superscript everything)
        footer = "\n\n&nbsp;\n\n*****\n\n*^I am a bot run by [\/u\/SupremeDesigner](https://www.reddit.com/user/SupremeDesigner) for /r/CodingHelp || This was an automated response || Posts with no flair will be deleted after two days*"
        footer = footer.replace(" ", " ^")
        
        # Generate Age
        today = datetime.now()
        postdate = datetime.fromtimestamp(submission.created_utc)
        age = today - postdate
        age_mins = (age.days * 24 * 60) + (age.seconds/60)
        age = age.days

        # If we haven't replied to this post before and older than 10 mins
        if submission.id not in posts_replied_to and age_mins >= 10:

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
            submission.add_comment("Please Add A Flair To Your Post!\n\nSuggested Flair: `["+flair+"]`" + footer)
##            print("NEW Post:", submission.title.translate(non_bmp_map), "\n\tFlair:", flair, "\n\n")

            # Store the current id into our list
            posts_replied_to.append(submission.id)

            # Write our updated list back to the file
            with open("codinghelp_posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + "\n")

        # If already replied and age >= 2, comment and delete
        elif age >= 2:

            # Output Alert
##            print("REMOVE Post:", submission.title.translate(non_bmp_map), "\n\tHas an age of", age, "days with no flair so is being deleted\n\n")
            
            # Reply to the post with deletion message
            submission.add_comment("Due to your post being submitted for two days or more without a flair, it has been deleted.\n\nWhen posting in future, make sure to add a flair once the post is submitted." + footer)

            # Flair Post
            submission.set_flair("[Removed]")

            # Lock post
            submission.lock()

            # Remove post
            submission.remove()
            
##        elif age_mins >= 10:
##            print("OLD Post:", submission.title.translate(non_bmp_map), "\n\tHas an age of", age, "days with no flair\n\n")

# Alert Completion
print("r/CodingHelp Bot Scan Completed")

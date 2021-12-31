import datetime

from conf import *

if RUN_CODING_HELP:
    try: from bots import codinghelp
    except Exception as e: print(e)

if RUN_R_ALL:
    try: from bots import rall
    except Exception as e: print(e)

if RUN_HUGS:
    try: from bots import hugs
    except Exception as e: print(e)

if RUN_DEL_COMMENTS:
    try: from bots import delcomments
    except Exception as e: print(e)

if RUN_SUBREDDIT_SNIPER:
    try: from bots import subredditsniper
    except Exception as e: print(e)

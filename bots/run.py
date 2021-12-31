import datetime

from config import *

if RUN_CODING_HELP:
    try: import codinghelp
    except Exception as e: print(e)

if RUN_R_ALL:
    try: import rall
    except Exception as e: print(e)

if RUN_HUGS:
    try: import hugs
    except Exception as e: print(e)

if RUN_DEL_COMMENTS:
    try: import delcomments
    except Exception as e: print(e)

if RUN_SUBREDDIT_SNIPER:
    try: import subredditsniper
    except Exception as e: print(e)

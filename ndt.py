#!/usr/bin/python

import ConfigParser
from datetime import datetime
import time
import sys

import praw


USER_AGENT = '/u/NobodyDoesThis by /u/karangoeluw'

MESSAGE = '''
Nope, it's just you.

------
[^NobodyDoesThis](https://github.com/karan/NobodyDoesThis) \
^bot ^by [^Karan ^Goel](http://www.goel.im/)
---
'''

SLEEP_AFTER_COMMENTING = 2 # seconds to sleep after commenting
IGNORE_FIRST_SUBMISSIONS = 100

r = praw.Reddit(user_agent=USER_AGENT)

config = ConfigParser.ConfigParser()
config.read('settings.cfg')
username = config.get('auth', 'username')
password = config.get('auth', 'password')
print '[*] Logging in as %s...' % username
r.login(username, password)
print '[*] Login successful...\n'

dae = r.get_subreddit('DoesAnybodyElse') # praw.objects.Subreddit

print '[*] Getting submissions...\n'

already_done = set()

posted = 0 # number of comments posted this session

for count, submission in enumerate(dae.get_hot(limit=None)):
    # skip the first few submissions
    if count > IGNORE_FIRST_SUBMISSIONS and submission.id not in already_done:
        already_done.add(submission.id)

        sys.stdout.write('\r[*] %d threads processed [*] %d comments posted' % 
            ((count - IGNORE_FIRST_SUBMISSIONS), posted))
        sys.stdout.flush()

        # make sure i haven't posted here earlier
        already_posted = False
        for comment in submission.comments:
            if comment.author == username:
                already_posted = True

        created = datetime.fromtimestamp(submission.created_utc) # epoch to datetime
        diff = (datetime.now() - created).total_seconds() / 60 / 60 / 24 # num days
        if (not already_posted and diff >= 3 and submission.score == 0): # post is older 3 days
            # score = 0
            comment = submission.add_comment(MESSAGE)
            #print '\n[*] %s' % submission.title
            #print '\tComment: %s' % comment.permalink
            time.sleep(SLEEP_AFTER_COMMENTING) # sleep for seconds after commenting
        #time.sleep(2) # to comply with rate limit

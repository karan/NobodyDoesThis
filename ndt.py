#!/usr/bin/env python

import ConfigParser
from datetime import datetime
import time

import praw


USER_AGENT = '/u/NobodyDoesThis by /u/karangoeluw'

MESSAGE = '''
Nope, it's just you.

------
[^NobodyDoesThis](https://github.com/karan/NobodyDoesThis) \
^bot ^by [^Karan ^Goel](http://www.goel.im/)
---
'''


r = praw.Reddit(user_agent=USER_AGENT)

print '[*] Reading config file...'
config = ConfigParser.ConfigParser()
config.read('settings.cfg')
username = config.get('auth', 'username')
password = config.get('auth', 'password')
print '[*] Logging in as %s...' % username
r.login(username, password)
print '[*] Login successful...\n'

dae = r.get_subreddit('DoesAnybodyElse') # praw.objects.Subreddit

print '[*] Getting submissions...\n'
submissions = dae.get_hot(limit=None) # get new posts

already_done = set()

for _, submission in enumerate(submissions):
    # skip the first 100 submissions
    if _ > 100 and submission.id not in already_done:
        already_done.add(submission.id)
        
        comments = submission.comments
        for comment in comments:
            try:
                if comment.author == username:
                    continue
            except AttributeError:
                pass
        
        print _, '[*] Thread: %s' % submission.title
        created = datetime.fromtimestamp(submission.created_utc) # epoch to datetime
        diff = (datetime.now() - created).total_seconds() / 60 / 60 / 24 # num days
        if (diff >= 3): # post is older 3 days
            if (submission.score == 0):
                # score = 0
                comment = submission.add_comment(MESSAGE)
                print '\tComment: %s' % comment.permalink
                print '\tSleeping for 10 minutes\n'
                time.sleep(600) # sleep for 10 mins
        time.sleep(2) # to comply with rate limit  

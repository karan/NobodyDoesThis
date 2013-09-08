#!/usr/bin/env python

import ConfigParser
from datetime import datetime
import time

import praw


USER_AGENT = '/u/NobodyDoesThis by /u/karangoeluw'

r = praw.Reddit(user_agent=USER_AGENT)

print '[*] Reading config file...'
config = ConfigParser.ConfigParser()
config.read('settings.cfg')
username = config.get('auth', 'username')
password = config.get('auth', 'password')
print '[*] Logging in...'
r.login(username, password)
print '[*] Login successful...\n'

dae = r.get_subreddit('DoesAnybodyElse') # praw.objects.Subreddit

print '[*] Getting submissions...\n'
submissions = dae.get_hot(limit=None) # get new posts

alread_done = set()

for submission in submissions:
    if submission.id not in alread_done:
        alread_done.add(submission.id)
        print '[*] Thread: %s' % submission.title
        created = datetime.fromtimestamp(submission.created_utc) # epoch to datetime
        diff = (datetime.now() - created).total_seconds() / 60 / 60 / 24 # num days
        if (diff >= 3): # post is older 3 days
            if (submission.score == 0):
                # score = 0
                comment = submission.add_comment('Nope, it\'s just you.')
                print '\tComment: %s' % comment.permalink
                print '\tSleeping for 10 minutes\n'
                time.sleep(600) # sleep for 10 mins
        #time.sleep(2) # to comply with rate limit
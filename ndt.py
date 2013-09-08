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
submissions = dae.get_new(limit=None) # get new posts

for submission in submissions:
    print '[*] Thread: %s' % submission.title
    created = datetime.fromtimestamp(submission.created_utc) # epoch to datetime
    diff = (created - datetime.now()).total_seconds()
    if (diff >= 604800): # post is older than a week
        if (submission.score == 0) and (not submission.hidden):
            # score = 0
            comment = submissions.add_comment('Nope, it\'s just you.')
            print '\tComment %s added' % comment.permalink
            submission.hide()
            #print '[*] Sleeping for 10 minutes\n'
            #time.sleep(600) # sleep for 10 mins
    time.sleep(2) # to comply with rate limit
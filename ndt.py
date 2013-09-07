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

dae = r.get_subreddit('DAE') # praw.objects.Subreddit

print '[*] Getting submissions...\n'
submissions = dae.get_new(limit=None) # get new posts

already_done = []

while True:
    for submission in submissions:
        if submission.id not in already_done:
            created = time.strftime('%Y-%m-%d %H:%M:%S', # epoch to string
                                    time.localtime(submission.created))
            created = datetime.strptime(created,
                                        '%Y-%m-%d %H:%M:%S') # str to datetime
            if ((created - datetime.now()).total_seconds() > 604800):
                # post is older than a week
                if (submission.num_comments == 0) or (submission.ups == submission.downs):
                    print '[*] Thread: %s' % submission.title
                    # 0 comments or 0 votes
                    comment = submissions.add_comment('Nope, it\'s just you.')
                    print '\tComment %s added' % comment.permalink
                    
                    print '[*] Sleeping for 10 minutes\n'
                    time.sleep(600) # sleep for 10 mins
        already_done.append(submission.id)
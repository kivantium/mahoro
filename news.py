#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import re
import time
import tweepy
import math
import datetime
import sys
import os

d = datetime.datetime.utcnow()
#Authorization
f = open(os.path.join(os.path.dirname(__file__), 'config.txt'))

data = f.read()
f.close()
lines = data.split('\n')

KEY = lines[0]
SECRET = lines[1]
ATOKEN = lines[2]
ASECRET = lines[3]

auth = tweepy.OAuthHandler(KEY, SECRET)
auth.set_access_token(ATOKEN, ASECRET)
api = tweepy.API(auth)
try:
    tweets = api.list_timeline('mitra_sun22', 'news', count=100)
    for tweet in tweets:
        message = tweet.text
        author = tweet.author.screen_name
        dif = d - tweet.created_at
        if dif.seconds >= 180 and dif.seconds < 240:
            if tweet.retweet_count > 50 and tweet.text.find('RT') == -1:
                api.update_status("https://twitter.com/{}/status/{}".format(tweet.author.screen_name, tweet.id))
except:
    pass

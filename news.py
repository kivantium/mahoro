#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import urllib2  
import re
import time
import tweepy
import math
import datetime
import sys

d = datetime.datetime.utcnow()
#Authorization
f = open('config.txt')
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
        if dif.seconds >= 300 and dif.seconds < 360:
            if tweet.retweet_count > 100:
                message = tweet.text
                author = tweet.author.screen_name
                if 'nhk' in author:
                    message += u'（NHK）'
                if 'nikkei' in author:
                    message += u'（日経新聞）'
                if 'YOL' in author:
                    message += u'（読売新聞）'
                if 'asahi' in author:
                    message += u'（朝日新聞）'
                if 'mainichi' in author:
                    message += u'（毎日新聞）'
                if '47news' in author:
                    message += u'（共同通信）'
                if 'Yahoo' in author:
                    message += u'（Yahoo）'
                if message.find('RT') == -1:
                    api.update_status(message)

except tweepy.error.TweepError, e:
    print "error response code: " + str(e.response.status)
    print "error message: " + str(e.response.reason)
    sys.exit()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TOKYO MXで放送するアニメを10分前に通知

import tweepy
import feedparser
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

url='http://cal.syoboi.jp/rss2.php?titlefmt=$(ChName),$(StTime),$(Mark)$(Title)%20$(SubTitleB)'

d = datetime.datetime.today()
d10 = d + datetime.timedelta(minutes=11)

item = feedparser.parse(url)

#Authorization
f = open('/home/kivantium/config.txt')
data = f.read()
f.close()
lines = data.split('\n')

KEY = lines[0]
SECRET = lines[1]
ATOKEN = lines[2]
ASECRET = lines[3]
#What to tweet
auth = tweepy.OAuthHandler(KEY, SECRET)
auth.set_access_token(ATOKEN, ASECRET)
api = tweepy.API(auth)

for entry in item['entries']:
    title = entry['title']
    time = entry['updated']
    info = title.split(',')
    t = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+09:00')

    if d <= t and d10 >= t:
        if info[0] == 'TOKYO MX':
            message = info[1]+'からTOKYO MXで'+info[2]+'が放送されます'
            api.update_status(message)

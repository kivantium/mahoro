#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TOKYO MXでその日の夜に放送するアニメを調べる

import tweepy
import feedparser
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

url='http://cal.syoboi.jp/rss2.php?titlefmt=$(ChName),$(StTime),$(Title)'

d = datetime.datetime.today()
d10 = d + datetime.timedelta(hours=9)

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

if d.hour >= 20:
    message = '今夜のTOKYO MXアニメ情報\n'
    for entry in item['entries']:
        title = entry['title']
        time = entry['updated']
        info = title.split(',')
        t = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+09:00')

        if d <= t and d10 >= t:
            if info[0] == 'TOKYO MX':
                message += info[1].split(' ')[1]
                message += ' '
                message += info[2][0:14]
                message += '\n'
    if len(message) > 140:
        api.update_status(message[0:140])
        api.update_status(message[140:])
    else:
        api.update_status(message)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import feedparser
import datetime
import os

url = 'http://cal.syoboi.jp/rss2.php?titlefmt=$(ChName),$(StTime),$(Title)'

d = datetime.datetime.today()
d10 = d + datetime.timedelta(hours=6)

item = feedparser.parse(url)

# Authorization
f = open(os.path.join(os.path.dirname(__file__), 'config.txt'))
data = f.read()
f.close()
lines = data.split('\n')

KEY = lines[0]
SECRET = lines[1]
ATOKEN = lines[2]
ASECRET = lines[3]

# What to tweet
auth = tweepy.OAuthHandler(KEY, SECRET)
auth.set_access_token(ATOKEN, ASECRET)
api = tweepy.API(auth)
showtime = []
showtitle = []

d = datetime.datetime.today()
message = '今夜のTOKYO MXアニメ情報\n'.format(hour=d.hour+1)
for entry in item['entries']:
    title = entry['title']
    time = entry['updated']
    info = title.split(',')
    t = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+09:00')

    if d <= t and d10 >= t:
        if info[0] == 'TOKYO MX':
            showtime.append(info[1].split(' ')[1])
            showtitle.append(info[2])
if len(showtime) > 0:
    for i in range(len(showtime)):
        if len(message+showtime[i]) > 140:
            api.update_status(message)
            message = ''
        message += showtime[i]
        message += ' '
        message += showtitle[i][:15]
        message += '\n'
    api.update_status(message)

showtime = []
showtitle = []
message = '今夜のテレビ東京アニメ情報\n'.format(hour=d.hour+1)
for entry in item['entries']:
    title = entry['title']
    time = entry['updated']
    info = title.split(',')
    t = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+09:00')

    if d <= t and d10 >= t:
        if info[0] == 'テレビ東京':
            showtime.append(info[1].split(' ')[1])
            showtitle.append(info[2])
if len(showtime) > 0:
    length = int(115/len(showtime))
    for i in range(len(showtime)):
        message += showtime[i]
        message += ' '
        message += showtitle[i][0:(length-7)]
        message += '\n'
    api.update_status(message)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import feedparser
import datetime
import os
import json

from mastodon import Mastodon

url = 'http://cal.syoboi.jp/rss2.php?titlefmt=$(ChName),$(StTime),$(Title)'

d = datetime.datetime.today()
d10 = d + datetime.timedelta(hours=6)

item = feedparser.parse(url)

# Authorization
with open("config.json") as f:
    data = json.load(f)

#Authorization
client = tweepy.Client(
    consumer_key=data["consumer_key"],
    consumer_secret=data["consumer_secret"],
    access_token=data["access_token"],
    access_token_secret=data["access_token_secret"]
)

api = Mastodon(
    api_base_url='https://mstdn.poyo.me',
    access_token=data["mastodon_token"])

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
            client.create_tweet(text=message)
            message = ''
        message += showtime[i]
        message += ' '
        message += showtitle[i][:15]
        message += '\n'
    client.create_tweet(text=message)

message = '今夜のTOKYO MXアニメ情報\n'
if len(showtime) > 0:
    for i in range(len(showtime)):
        message += showtime[i]
        message += ' '
        message += showtitle[i]
        message += '\n'
    api.toot(message)

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
    client.create_tweet(text=message)

message = '今夜のテレビ東京アニメ情報\n'
if len(showtime) > 0:
    length = int(115/len(showtime))
    for i in range(len(showtime)):
        message += showtime[i]
        message += ' '
        message += showtitle[i]
        message += '\n'
    api.toot(message)

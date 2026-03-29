#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tweepy
import feedparser
import datetime
import os
import json

from mastodon import Mastodon

url = 'http://cal.syoboi.jp/rss2.php?titlefmt=$(ChName),$(StTime),$(Mark),$(Title)'

d = datetime.datetime.today()
d10 = d + datetime.timedelta(hours=6)

item = feedparser.parse(url)

# Authorization
with open("/home/kivantium/mahoro/config.json") as f:
    data = json.load(f)

#Authorization
api = Mastodon(
    api_base_url='https://mstdn.poyo.me',
    access_token=data["mastodon_token"])

showtime = []
showtitle = []

d = datetime.datetime.today()
show_list = []
for entry in item['entries']:
    title = entry['title']
    time = entry['updated']
    channel, start, mark, title = title.split(',')
    if mark == "【新】":
        title = mark + title

    t = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+09:00')
    if d <= t and d10 >= t:
        show_list.append({"channel": channel, "time": start.split(' ')[1], "title": title})


message = '今夜のアニメ情報\n'
for c in ["TOKYO MX", "TBS", "テレビ東京"]:
    show_by_channel = []
    for show in show_list:
        if show["channel"] == c:
            show_by_channel.append(show)
    if show_by_channel:
        message += c + "\n"
        for show in show_by_channel:
            message += f"{show['time']} {show['title']}\n"
        message += "\n"

try:
    api.toot(message)
except:
    pass

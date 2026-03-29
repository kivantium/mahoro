#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import feedparser
import datetime
import json

from zoneinfo import ZoneInfo
from mastodon import Mastodon

JST = ZoneInfo("Asia/Tokyo")

url = 'http://cal.syoboi.jp/rss2.php?titlefmt=$(ChName),$(StTime),$(Mark),$(Title)'

item = feedparser.parse(url)

# Authorization
with open("/home/kivantium/mahoro/config.json") as f:
    data = json.load(f)

api = Mastodon(
    api_base_url='https://mstdn.poyo.me',
    access_token=data["mastodon_token"])

now = datetime.datetime.now(JST)
until = now + datetime.timedelta(hours=6)

show_list = []
for entry in item['entries']:
    title = entry['title']
    time_str = entry['updated']
    channel, start, mark, title = title.split(',')
    if mark == "【新】":
        title = mark + title

    t = datetime.datetime.fromisoformat(time_str)
    if t.tzinfo is None:
        t = t.replace(tzinfo=JST)

    if now <= t <= until:
        show_list.append({"channel": channel, "time": start.split(' ')[1], "title": title})

exclude_keywords = ["Abema", "BS", "AT-X", "YouTube", "文化放送", "アニマックス"]

seen = set()
channels = []
for show in show_list:
    ch = show["channel"]
    if ch not in seen:
        seen.add(ch)
        if not any(kw in ch for kw in exclude_keywords):
            channels.append(ch)

message = '今夜のアニメ情報\n'
for c in channels:
    show_by_channel = [show for show in show_list if show["channel"] == c]
    if show_by_channel:
        message += c + "\n"
        for show in show_by_channel:
            message += f"{show['time']} {show['title']}\n"
        message += "\n"

try:
    api.toot(message)
except:
    pass

#!/usr/bin/python
# -*- coding: utf-8 -*-

import jholiday
from time import sleep
import urllib2  
import re
import time
import tweepy
import math
import datetime

def isOpen(today):
    tommorrow = today + datetime.timedelta(days=1)
    yesterday = today - datetime.timedelta(days=1)
    if today.weekday() >= 5 or jholiday.holiday_name(date=today) is not None or (jholiday.holiday_name(date=tommorrow) is not None and jholiday.holiday_name(date=yesterday)) or (today.month==1 and today.day <= 3) or (today.month==12 and today.day == 31) :
        return False
    else:
        return True
#時間
d = datetime.datetime.today()
message = '{month}月{day}日{hour}時{minute}分をお知らせします。\n\n'.format(month=str(d.month), day=str(d.day), hour=str(d.hour).zfill(2), minute=str(d.minute).zfill(2))

#円相場
url = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
res = urllib2.urlopen(url)  
data = res.read()
tmp = re.search('<td class="stoksPrice">(.*)</td>', data, re.U)
dollar = tmp.group(1)
dollar = round(float(dollar), 2)
message += "円相場: 1ドル{price}円\n".format(price=str(dollar))

today = datetime.date.today()
if isOpen(today) and d.hour >= 10 and d.hour <= 15:
    #日経平均
	url = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=998407"
	res = urllib2.urlopen(url)  
	data = res.read()
	tmp = re.search('<td class="stoksPrice">(.*)</td>', data, re.U)
	nikkei = tmp.group(1)
	nikkei = nikkei.replace(',','')
	tmp = re.search('前日比</span><span class=".*">(.*)（.*）</span>', data, re.U)
	nikkei_change= tmp.group(1)
	message += "日経平均: {price}円 (前日比{change}円)\n".format(price=str(nikkei), change=str(nikkei_change))

    #TOPIX
	url = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=998405"
	res = urllib2.urlopen(url)  
	data = res.read()
	tmp = re.search('<td class="stoksPrice">(.*)</td>', data, re.U)
	topix = tmp.group(1)
	topix = topix.replace(',','')
	tmp = re.search('前日比</span><span class=".*">(.*)（.*）</span>', data, re.U)
	topix_change= tmp.group(1)
	message += "TOPIX: {price} (前日比{change})".format(price=str(topix), change=str(topix_change))
#Authorization
f = open('config.txt')
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
print message
api.update_status(message)

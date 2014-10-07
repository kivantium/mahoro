#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import urllib2  
import re
import time
import tweepy
import math
import datetime

#時間
d = datetime.datetime.today()
if d.hour >= 6 and d.hour <= 9:
	message = 'おはようございます。'
elif d.hour >= 10 and d.hour <= 14:
	message = 'こんにちは。'
else:
	message =  'お疲れさまです。'
message += '%s月%s日%s時%s分をお知らせします。\n' % (d.month, d.day, d.hour, d.minute)

#円相場
url = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=usdjpy"
res = urllib2.urlopen(url)  
data = res.read()
tmp = re.search('<td class="stoksPrice">(.*)</td>', data, re.U)
dollar = tmp.group(1)
dollar = round(float(dollar), 2)
message += "ただいまの円相場は1ドル"+str(dollar)+"円"+"です。\n"

#日経平均
if d.weekday() <=5 and d.hour >= 10 and d.hour <= 15:
	url = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=998407"
	res = urllib2.urlopen(url)  
	data = res.read()
	tmp = re.search('<td class="stoksPrice">(.*)</td>', data, re.U)
	nikkei = tmp.group(1)
	nikkei = nikkei.replace(',','')
	tmp = re.search('前日比</span><span class=".*">(.*)（.*）</span>', data, re.U)
	nikkei_change= tmp.group(1)
	message += "日経平均株価は"+nikkei+"円"+"(前日比"+nikkei_change+"円)になっています。"

#Authorization
f = open('/home/mahoro/tweetmaid/config.txt')
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
api.update_status(message)


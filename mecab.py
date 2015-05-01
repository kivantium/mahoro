#!/usr/bin/env python
#-*- coding:utf-8 -*-

# リプライに対して形態素解析の結果を返す

from tweepy import *
import urllib2  
import MeCab
import re
import random
import sys

#Authorization
f = open('config.txt')
data = f.read()
f.close()
lines = data.split('\n')

 #エンコード設定
reload(sys)
sys.setdefaultencoding('utf-8')

def wakati(text):
    print text
    t = MeCab.Tagger("-Owakati -d /usr/lib/mecab/dic/mecab-ipadic-neologd")
    m = t.parse(text)
    return m.replace(' ','/')


def get_oauth():
	consumer_key = lines[0]
	consumer_secret = lines[1]
	access_key = lines[2]
	access_secret = lines[3]
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	return auth

class StreamListener(StreamListener):
    def on_status(self, status):
		if status.in_reply_to_screen_name=='mitra_sun22':
			print status.text
			message = '@'+status.author.screen_name+' '
			string = status.text.replace('@mitra_sun22', '').encode('utf-8')
			if 'アステラス' in status.text:
			   url = "http://stocks.finance.yahoo.co.jp/stocks/detail/?code=4503"
			   res = urllib2.urlopen(url)  
			   data = res.read()
			   tmp = re.search('<td class="stoksPrice">(.*)</td>', data, re.U)
			   dollar = tmp.group(1)
			   tmp = re.search('前日比</span><span class=".*">(.*)（.*）</span>', data, re.U)
			   change= tmp.group(1)
			   message += "アステラス製薬の株価は{price}円(前日比: {tmp})です".format(price=str(dollar), tmp=str(change))
			else:
			   for line in string.split('\n'):
			       message += wakati(line)
			       message += '\n'
			message = message.decode("utf-8")
			try:
				api.update_status(status=message[0:140], in_reply_to_status_id=status.id)
			except TweepError, e:
				print "error response code: " + str(e.response.status)
				print "error message: " + str(e.response.reason)

auth = get_oauth()
api = API(auth)
stream = Stream(auth, StreamListener(), secure=True)
print "Start Streaming!"
stream.userstream()

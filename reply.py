#-*- coding: utf-8 -*-
#!/usr/bin/python

import codecs
from tweepy import *
import MeCab
import random

#Authorization
f = codecs.open('/home/mahoro/tweetmaid/config.txt','r','utf-8')
data = f.read()
f.close()
lines = data.split('\n')
f = codecs.open('/home/mahoro/tweetmaid/keyword.txt','r','utf-8')
data = f.read()
f.close()
keywords = data.split('\n')

tagger = MeCab.Tagger('-Ochasen')
def analyze(message):
	node = tagger.parseToNode(message)
	if '進捗どうですか' in message:
		return '進捗ダメです'
	if 'いつ' in message or 'どこ' in message or '誰' in message or 'だれ' in message or 'なに' in message or '何' in message or 'どう' in message or 'なぜ' in message or 'なんで' in message or 'どの' in message:
		return 'その質問は難しすぎます >' + message
	while node:
		if node.surface == 'です' and node.feature.split(",")[0] == '助動詞':
			if node.next.surface == 'か':
				if node.prev.feature.split(",")[0] == '形容詞':
					message = message.replace('いですか', 'くありません')
				else:
					message = message.replace('ですか', 'ではありません')
				message = message.replace('あなたは', '私は')
				message = message.replace('まほろさんは', '私は')
				message = message.replace('?', '')
				message = message.replace('？', '')
				return message
		if node.surface == 'ます' and node.feature.split(",")[0] == '助動詞':
			if node.next.surface == 'か':
				message = message.replace('ますか', 'ません')
				message = message.replace('あなたは', '私は')
				message = message.replace('まほろさんは', '私は')
				message = message.replace('?', '')
				message = message.replace('？', '')
				return message
		node = node.next
	return '申し訳ないのですが、お答えできません >' + message

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
		message = status.text
		message = message.replace('&lt;', '<')
		message = message.replace('&gt;', '>')
		message = message.replace('&amp;', '&')
		author = status.author.screen_name
		if status.in_reply_to_screen_name=='mitra_sun22':
			message = message.replace('@mitra_sun22 ', '')
			message = message.encode("utf-8")
			message = analyze(message)
			message = message.decode("utf-8")
			message = '@'+author+' '+message
			try:
				api.update_status(message[0:140], in_reply_to_status_id = status.id)
			except tweepy.error.TweepError, e:
				print "error response code: " + str(e.response.status)
				print "error message: " + str(e.response.reason)
		if author=='kivantium' or author=='akemi_mkr':
			message = message.encode("utf-8")
			node = tagger.parseToNode(message)
			message = message.decode("utf-8")
			while node:
				if node.feature.split(",")[0] == "名詞":
					word = random.choice(keywords)
					print node.surface, word
					message = message.replace(node.surface.decode("utf-8"), word)
				node = node.next
			try:
				print message
				api.update_status(message[0:140])
			except tweepy.error.TweepError, e:
				print "error response code: " + str(e.response.status)
				print "error message: " + str(e.response.reason)
auth = get_oauth()
api = API(auth)
stream = Stream(auth, StreamListener(), secure=True)
print "Start Streaming!"
stream.userstream()

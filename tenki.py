#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy
import urllib2
import datetime
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET

url  = "http://www.drk7.jp/weather/xml/13.xml"
d = datetime.datetime.today()
today = '{year}/{month}/{day}'.format(year=d.year, month=str(d.month).zfill(2), day=str(d.day).zfill(2))
content = '{month}月{day}日{hour}時 東京の天気予報です。\n'.format(month=d.month, day=d.day, hour=d.hour)

res = urllib2.urlopen(url)
feed = res.read()

tree = ET.fromstring(feed)
weather = tree.findall(".//area[4]/info[@date='{date}']/weather".format(date=today))
content += '今日の天気は{tenki}\n'.format(tenki=weather[0].text.encode('utf-8'))
chance = tree.findall(".//area[4]/info[@date='{date}']/rainfallchance/period".format(date=today))
content += '降水確率は午前{am}%、午後{pm}%、夜{night}%\n'.format(am=chance[1].text, pm=chance[2].text, night=chance[3].text)
temp = tree.findall(".//area[4]/info[@date='{date}']/temperature/range".format(date=today))
content += '最低気温は{min}℃、最高気温は{max}℃\n'.format(min=temp[1].text, max=temp[0].text)
content += 'http://www.jma.go.jp/jp/yoho/319.html'

image = Image.new('RGB', (800, 450), (255, 255, 255))

draw = ImageDraw.Draw(image)
font_50 = ImageFont.truetype('GenShinGothic-P-Regular.ttf', 50, encoding='unic')
font_40 = ImageFont.truetype('GenShinGothic-P-Regular.ttf', 40, encoding='unic')
font_30 = ImageFont.truetype('GenShinGothic-P-Regular.ttf', 30, encoding='unic')
font_26 = ImageFont.truetype('GenShinGothic-P-Regular.ttf', 26, encoding='unic')
font_20 = ImageFont.truetype('GenShinGothic-P-Regular.ttf', 20, encoding='unic')


draw.text((30, 20), u'{}月{}日 東京の天気'.format(d.month, d.day), font=font_50, fill=(0,0,0))

if weather[0].text.find(u'雪') > -1:
    emoji = Image.open('snowy.png')
elif weather[0].text.find(u'雨') > -1:
    emoji = Image.open('rainy.png')
elif weather[0].text.find(u'くもり') > -1:
    emoji = Image.open('clowdy.png')
else:
    emoji = Image.open('sunny.png')

emoji = emoji.resize((150, 150))
image.paste(emoji, (60, 150))

draw.text((60, 330), u'{}'.format(weather[0].text.center(15)), font=font_30, fill=(0,0,0))

draw.text((300, 130), u'最高 {}℃'.format(temp[0].text), font=font_40, fill=(200,50,50))
draw.text((300, 190), u'最低 {}℃'.format(temp[1].text), font=font_40, fill=(50,50,200))

x = 300
y = 280
w = 480
h = 120

draw.line((x,y,x+w,y), (150,150,150), 1)
draw.line((x,y+h,x+w,y+h), (150,150,150), 1)
draw.line((x,y,x,y+h), (150,150,150), 1)
draw.line((x+w,y,x+w,y+h), (150,150,150), 1)
draw.line((x,y+h/2,x+w,y+h/2), (150,150,150), 1)
draw.line((x+w*1/5,y,x+w*1/5,y+h), (150,150,150), 1)
draw.line((x+w*2/5,y,x+w*2/5,y+h), (150,150,150), 1)
draw.line((x+w*3/5,y,x+w*3/5,y+h), (150,150,150), 1)
draw.line((x+w*4/5,y,x+w*4/5,y+h), (150,150,150), 1)

draw.text((x+15+2, y+10), u'時間', font=font_30, fill=(50,50,50))
draw.text((x+w*1/5+15, y+12), u'00-06', font=font_26, fill=(50,50,50))
draw.text((x+w*2/5+15, y+12), u'06-12', font=font_26, fill=(50,50,50))
draw.text((x+w*3/5+15, y+12), u'12-18', font=font_26, fill=(50,50,50))
draw.text((x+w*4/5+15, y+12), u'18-24', font=font_26, fill=(50,50,50))

draw.text((x+8, y+h/2+15), u'降水確率', font=font_20, fill=(50,50,50))
draw.text((x+w*1/5+20, y+h/2+10), u'{}%'.format(chance[0].text.rjust(2)), font=font_30, fill=(50,50,50))
draw.text((x+w*2/5+20, y+h/2+10), u'{}%'.format(chance[1].text.rjust(2)), font=font_30, fill=(50,50,50))
draw.text((x+w*3/5+20, y+h/2+10), u'{}%'.format(chance[2].text.rjust(2)), font=font_30, fill=(50,50,50))
draw.text((x+w*4/5+20, y+h/2+10), u'{}%'.format(chance[3].text.rjust(2)), font=font_30, fill=(50,50,50))

image.save('weather.png')

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
api.update_with_media('weather.png', status=content)

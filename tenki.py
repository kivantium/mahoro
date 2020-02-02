#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import tweepy
import datetime
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
import requests
import os

url  = "http://www.drk7.jp/weather/xml/13.xml"
d = datetime.datetime.today()
today = '{year}/{month}/{day}'.format(year=d.year, month=str(d.month).zfill(2), day=str(d.day).zfill(2))
content = '今日{}時の天気予報です。\n'.format(d.hour)

response = requests.get(url)
response.encoding = response.apparent_encoding
feed = response.text

tree = ET.fromstring(feed)
weather = tree.findall(".//area[4]/info[@date='{date}']/weather".format(date=today))
content += '{}月{}日の東京の天気は{}\n'.format(d.month, d.day, weather[0].text)
chance = tree.findall(".//area[4]/info[@date='{date}']/rainfallchance/period".format(date=today))
content += '降水確率は午前{am}%、午後{pm}%、夜{night}%\n'.format(am=chance[1].text, pm=chance[2].text, night=chance[3].text)
temp = tree.findall(".//area[4]/info[@date='{date}']/temperature/range".format(date=today))
content += '最低気温は{min}℃、最高気温は{max}℃\n'.format(min=temp[1].text, max=temp[0].text)
content += 'http://www.jma.go.jp/jp/yoho/319.html'

image = Image.new('RGB', (800, 450), (255, 255, 255))

draw = ImageDraw.Draw(image)
font_path = os.path.join(os.path.dirname(__file__), 'GenShinGothic-P-Regular.ttf')
font_50 = ImageFont.truetype(font_path, 50)
font_40 = ImageFont.truetype(font_path, 40)
font_30 = ImageFont.truetype(font_path, 30)
font_26 = ImageFont.truetype(font_path, 26)
font_20 = ImageFont.truetype(font_path, 20)


draw.text((30, 20), u'{}月{}日 東京の天気'.format(d.month, d.day), font=font_50, fill=(0,0,0))

if weather[0].text.find(u'雪') > -1:
    emoji = Image.open(os.path.join(os.path.dirname(__file__), 'snowy.png'))
elif weather[0].text.find(u'雨') > -1:
    emoji = Image.open(os.path.join(os.path.dirname(__file__), 'rainy.png'))
elif weather[0].text.find(u'くもり') > -1:
    emoji = Image.open(os.path.join(os.path.dirname(__file__), 'clowdy.png'))
else:
    emoji = Image.open(os.path.join(os.path.dirname(__file__), 'sunny.png'))

emoji = emoji.resize((150, 150))
image.paste(emoji, (60, 150))

fill = 5-len(weather[0].text)/2
draw.text((0, 330), u'{}{}{}'.format(u'　'*int(fill), weather[0].text, u'　'*int(fill)), font=font_30, fill=(0,0,0))

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

image.save(os.path.join(os.path.dirname(__file__), 'weather.png'))

#Authorization
f = open(os.path.join(os.path.dirname(__file__), 'config.txt'))
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
api.update_with_media(os.path.join(os.path.dirname(__file__), 'weather.png'), status=content)

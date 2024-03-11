#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import jholiday
from time import sleep
import re
import time
import tweepy
import math
import datetime
import json
import requests
import os
from bs4 import BeautifulSoup
import holidays
import jholiday
from pytz import timezone
import python_bitbankcc

import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

def isOpen(today):
    tommorrow = today + datetime.timedelta(days=1)
    yesterday = today - datetime.timedelta(days=1)
    if today.weekday() >= 5 or jholiday.holiday_name(date=today) is not None or (jholiday.holiday_name(date=tommorrow) is not None and jholiday.holiday_name(date=yesterday)) or (today.month==1 and today.day <= 3) or (today.month==12 and today.day == 31) :
        return False
    else:
        return True
#時間
d = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
tz = timezone('US/Eastern')
ustime = datetime.datetime.now(tz)
message = '{month}月{day}日{hour}時{minute}分をお知らせします。\n'.format(month=str(d.month), day=str(d.day), hour=str(d.hour).zfill(2), minute=str(d.minute).zfill(2))
message += 'ニューヨーク時間: {}月{}日{}時{}分\n\n'.format(ustime.month, ustime.day, str(ustime.hour).zfill(2), str(ustime.minute).zfill(2))

today = datetime.date.today()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
if isOpen(today) and d.hour >= 10 and d.hour <= 15:
    #日経平均
    try:
        res = requests.get('https://finance.yahoo.com/quote/%5EN225?p=%5EN225', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        nikkei_price = soup.find('fin-streamer', {'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)','data-symbol':'^N225'}).string
        nikkei_change = soup.find('fin-streamer', {'class':'Fw(500) Pstart(8px) Fz(24px)','data-symbol':'^N225'}).string
        message += "日経平均: {price}円 (前日比{change}円)\n".format(price=(nikkei_price), change=str(nikkei_change))
    except:
        pass

    #TOPIX
    #rest = requests.get('http://stocks.finance.yahoo.co.jp/stocks/detail/?code=998405')
    #soupt = BeautifulSoup(rest.text, 'html.parser')
    #topix_price = soupt.find_all('td', class_='stoksPrice')[1].get_text()
    #topix_change = soupt.find('span', class_='icoUpGreen yjMSt').get_text().split('（')[0]
    #message += "TOPIX: {price} (前日比{change})\n".format(price=str(topix_price), change=str(topix_change))

us_holidays = holidays.UnitedStates()

if ustime.date().weekday() <= 4 and ustime.date() not in us_holidays and ustime.hour >= 10 and ustime.hour <= 16:
    try:
        res = requests.get('https://finance.yahoo.com/quote/%5EDJI?p=%5EDJI', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        dow_price = soup.find('fin-streamer', {'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)','data-symbol':'^DJI'}).string
        dow_change = soup.find('fin-streamer', {'class':'Fw(500) Pstart(8px) Fz(24px)','data-symbol':'^DJI'}).string
        message += "ダウ平均: {price}ドル (前日比{change}ドル)\n".format(price=(dow_price), change=str(dow_change))
        #spc_price = soup.find('span', {'data-reactid':'303'}).get_text()
        #spc_change = soup.find('span', {'data-reactid':'305'}).get_text()
        #message += "S&P 500: {price} (前日比{change})\n".format(price=(spc_price), change=str(spc_change))
    except:
        pass

try:
    res = requests.get('https://finance.yahoo.com/quote/JPY%3DX?p=JPY%3DX', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    dollar = soup.find('fin-streamer', {'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).string
    message += "1ドル: {:.2f}円\n".format(float(dollar))
except:
    try:
        res = requests.get('https://finance.yahoo.com/currencies', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        search = re.compile('.*USD/JPY.*')
        dollar = soup.find(text=search).find_next().text
        message += "1ドル: {:.2f}円\n".format(float(dollar))
    except:
        pass

btc = requests.get('https://api.bitflyer.jp/v1/ticker?product_code=BTC_JPY').json()['ltp']
message += "現在のビットコイン価格は{price}円です".format(price=str(btc))

today = datetime.datetime.utcnow()
yesterday = today - datetime.timedelta(days=1)
pub = python_bitbankcc.public()
df = pd.DataFrame({'Open': [], 'High':[], 'Low':[], 'Close':[], 'Volume':[]})

value = pub.get_candlestick('btc_jpy', '15min', yesterday.strftime('%Y%m%d'))
for o, h, l, c, v, ut in value["candlestick"][0]["ohlcv"]:
    dt = pd.to_datetime(ut, unit='ms')
    dt_jst = datetime.datetime.fromtimestamp(ut/1000, datetime.timezone(datetime.timedelta(hours=9)))
    df.loc[dt] = [int(o), int(h), int(l), int(c), float(v)]

value = pub.get_candlestick('btc_jpy', '15min', today.strftime('%Y%m%d'))
for o, h, l, c, v, ut in value["candlestick"][0]["ohlcv"]:
    dt = pd.to_datetime(ut, unit='ms')
    dt_jst = datetime.datetime.fromtimestamp(ut/1000, datetime.timezone(datetime.timedelta(hours=9)))
    df.loc[dt] = [int(o), int(h), int(l), int(c), float(v)]

df['ema_12'] = df['Close'].ewm(span=12).mean()
df['ema_26'] = df['Close'].ewm(span=26).mean()
df['macd'] = df['ema_12'] - df['ema_26']
df['signal'] = df['macd'].ewm(span=9).mean()
df['macdhist'] = df['macd']-df['signal']
df['macdhist_ema3'] = df['macdhist'].ewm(span=3).mean()


df = df.tz_localize('UTC').tz_convert('Asia/Tokyo')
df = df[-49:-1]
apds = [ mpf.make_addplot(df['macdhist'], type='bar', width=1.0, panel=1, color='gray', alpha=0.5, ylabel='macdhist'),
         mpf.make_addplot(df['macdhist_ema3'], width=1.0, panel=1, alpha=0.5) ]

filename = os.path.join(os.path.dirname(__file__), 'candlestick.png')
#mpf.plot(df, type='candle', figratio=(16, 9), style='yahoo', savefig=filename, addplot=apds)
mpf.plot(df, type='candle', figratio=(16, 9), style='yahoo', savefig=filename)

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
api.update_with_media(filename, status=message)

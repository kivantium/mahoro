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

from mastodon import Mastodon


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
        res = requests.get("https://query2.finance.yahoo.com/v8/finance/chart/%5EN225?range=1m", headers=headers, timeout=5).json()
        nikkei_price = float(res['chart']['result'][0]['meta']['regularMarketPrice'])
        nikkei_previousClose = float(res['chart']['result'][0]['meta']['previousClose'])
        nikkei_change = nikkei_price - nikkei_previousClose
        message += "日経平均: {price}円 (前日比{sign}{change:.2f}円)\n".format(price=str(nikkei_price), sign=("+" if nikkei_change > 0 else ""), change=nikkei_change)
    except:
        try:
            res = requests.get('https://finance.yahoo.com/quote/%5EN225?p=%5EN225', headers=headers, timeout=5)
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
        res = requests.get("https://query2.finance.yahoo.com/v8/finance/chart/%5EDJI?range=1m", headers=headers, timeout=5).json()
        dow_price = float(res['chart']['result'][0]['meta']['regularMarketPrice'])
        dow_previousClose = float(res['chart']['result'][0]['meta']['previousClose'])
        dow_change = dow_price - dow_previousClose
        message += "ダウ平均: {price}ドル (前日比{sign}{change:.2f}ドル)\n".format(price=str(dow_price), sign=("+" if dow_change > 0 else ""), change=dow_change)
    except:
        try:
            res = requests.get('https://finance.yahoo.com/quote/%5EDJI?p=%5EDJI', headers=headers, timeout=5)
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
    res = requests.get("https://query2.finance.yahoo.com/v8/finance/chart/JPY%3DX?p=JPY%3DX'?range=1m", headers=headers, timeout=5).json()
    dollar = res['chart']['result'][0]['meta']['regularMarketPrice']
    message += "1ドル: {:.2f}円\n".format(float(dollar))
except:
    try:
        res = requests.get('https://finance.yahoo.com/quote/JPY%3DX?p=JPY%3DX', headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        dollar = soup.find('fin-streamer', {'class':'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).string
        message += "1ドル: {:.2f}円\n".format(float(dollar))
    except:
        try:
            res = requests.get('https://finance.yahoo.com/currencies', headers=headers, timeout=5)
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

with open("config.json") as f:
    data = json.load(f)


#Authorization
client = tweepy.Client(
    consumer_key=data["consumer_key"],
    consumer_secret=data["consumer_secret"],
    access_token=data["access_token"],
    access_token_secret=data["access_token_secret"]
)

client.create_tweet(text=message)

api = Mastodon(
    api_base_url='https://mstdn.poyo.me',
    access_token=data["mastodon_token"])

api.status_post(message)

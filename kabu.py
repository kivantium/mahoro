#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import tweepy
import datetime
import json
import requests
import holidays
import jholiday
from pytz import timezone
from mastodon import Mastodon
import asyncio
from playwright.async_api import async_playwright
import random

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

async def fetch_yahoo_api(message):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale="ja-JP", user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
        page = await context.new_page()
        # セッションCookieを得る
        await page.goto("https://finance.yahoo.co.jp")
        await page.wait_for_timeout(3000)  # 3秒待機でJSとCookie取得

        if isOpen(today) and d.hour >= 10 and d.hour <= 16:
            try:
                time.sleep(5*random.random())
                nikkei_url = "https://query2.finance.yahoo.com/v8/finance/chart/^N225?range=1m"
                nikkei_response = await page.goto(nikkei_url)
                nikkei_body = await nikkei_response.text()
                nikkei_data = json.loads(nikkei_body)
                nikkei_price = float(nikkei_data['chart']['result'][0]['meta']['regularMarketPrice'])
                nikkei_previousClose = float(nikkei_data['chart']['result'][0]['meta']['previousClose'])
                nikkei_change = nikkei_price - nikkei_previousClose
                message += "日経平均: {price}円 (前日比{sign}{change:.2f}円)\n".format(price=str(nikkei_price), sign=("+" if nikkei_change > 0 else ""), change=nikkei_change)
            except:
                pass

        us_holidays = holidays.UnitedStates()

        if ustime.date().weekday() <= 4 and ustime.date() not in us_holidays and ustime.hour >= 10 and ustime.hour <= 16:
            try:
                time.sleep(5*random.random())
                dow_url = "https://query2.finance.yahoo.com/v8/finance/chart/%5EDJI?range=1m"
                dow_response = await page.goto(dow_url)
                dow_body = await dow_response.text()
                dow_data = json.loads(dow_body)
                dow_price = float(dow_data['chart']['result'][0]['meta']['regularMarketPrice'])
                dow_previousClose = float(dow_data['chart']['result'][0]['meta']['previousClose'])
                dow_change = dow_price - dow_previousClose
                message += "ダウ平均: {price}ドル (前日比{sign}{change:.2f}ドル)\n".format(price=str(dow_price), sign=("+" if dow_change > 0 else ""), change=dow_change)
            except:
                pass

            try:
                time.sleep(5*random.random())
                nasdaq_url = "https://query2.finance.yahoo.com/v8/finance/chart/%5EIXIC?range=1m"
                nasdaq_response = await page.goto(nasdaq_url)
                nasdaq_body = await nasdaq_response.text()
                nasdaq_data = json.loads(nasdaq_body)
                nasdaq_price = float(nasdaq_data['chart']['result'][0]['meta']['regularMarketPrice'])
                nasdaq_previousClose = float(nasdaq_data['chart']['result'][0]['meta']['previousClose'])
                nasdaq_change = nasdaq_price - nasdaq_previousClose
                message += "NASDAQ: {price}円 (前日比{sign}{change:.2f}円)\n".format(price=str(nasdaq_price), sign=("+" if nasdaq_change > 0 else ""), change=nasdaq_change)
            except:
                pass

            try:
                time.sleep(5*random.random())
                nikkei_url = "https://query2.finance.yahoo.com/v8/finance/chart/NIY%3DF?range=1m"
                nikkei_response = await page.goto(nikkei_url)
                nikkei_body = await nikkei_response.text()
                nikkei_data = json.loads(nikkei_body)
                nikkei_price = float(nikkei_data['chart']['result'][0]['meta']['regularMarketPrice'])
                nikkei_previousClose = float(nikkei_data['chart']['result'][0]['meta']['previousClose'])
                nikkei_change = nikkei_price - nikkei_previousClose
                message += "日経平均先物: {price}円 (前日比{sign}{change:.2f}円)\n".format(price=str(nikkei_price), sign=("+" if nikkei_change > 0 else ""), change=nikkei_change)
            except:
                pass

        try:
            time.sleep(5*random.random())
            yen_url = "https://query2.finance.yahoo.com/v8/finance/chart/JPY%3DX?p=JPY%3DX'?range=1m"
            yen_response = await page.goto(nikkei_url)
            yen_body = await yen_response.text()
            yen_data = json.loads(yen_body)
            yen_price = float(yen_data['chart']['result'][0]['meta']['regularMarketPrice'])
            message += "1ドル: {:.2f}円\n".format(yen_price)
        except:
            pass

        await browser.close()

message = asyncio.run(fetch_yahoo_api(message))

btc = requests.get('https://api.bitflyer.jp/v1/ticker?product_code=BTC_JPY').json()['ltp']
message += "現在のビットコイン価格は{price}円です".format(price=str(btc))

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

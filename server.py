#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import os
import sys
import traceback

from flask import Flask, flash, request, redirect, url_for
import magic
from tweepy import *
from werkzeug.utils import secure_filename
import subprocess

#Authorization
f = open(os.path.join(os.path.dirname(__file__), 'config2.txt'))
data = f.read()
f.close()
lines = data.split('\n')

def get_oauth():
    consumer_key = lines[0]
    consumer_secret = lines[1]
    access_key = lines[2]
    access_secret = lines[3]
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return auth

auth = get_oauth()
api = API(auth)

ALLOWED_MIMETYPE = set(['image/jpeg', 'image/gif', 'image/png', 'image/webp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.dirname(__file__)
#app.config['MAX_CONTENT_LENGTH'] = 10240 *  1024 

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return '''
            <!doctype html>
            <html>
            <head>
            <title>ファイルを選択してください</title>
            </head>
            <body>
            <p>ファイルを選択してください</p>
            </body>
            </html>
            '''
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return '''
            <!doctype html>
            <html>
            <head>
            <title>ファイルを選択してください</title>
            </head>
            <body>
            <p>ファイルを選択してください</p>
            </body>
            </html>
            '''
        if file:
            filename = secure_filename(file.filename)
            _, ext = os.path.splitext(file.filename)
            current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            filename = os.path.join(app.config['UPLOAD_FOLDER'], current_time+ext)
            file.save(filename)
            mimetype = magic.from_file(filename, mime=True)
            if mimetype not in ALLOWED_MIMETYPE:
                return '''
                <!doctype html>
                <html>
                <head>
                <meta charset="utf-8"/>
                <title>アップロードされました</title>
                </head>
                <body>
                <p>エラーが起こりました。JPEG, GIF, PNG, WebP以外の画像をアップロードしていませんか？</p>
                </body>
                </html>
                '''
            if ext == '':
                ext = '.' + mimetype.split('/')[1]
                os.rename(filename, filename+ext)
                filename = filename + ext
            try:
                if os.path.getsize(filename) > 700*1000 or mimetype == 'image/webp':
                    subprocess.call('convert {} -thumbnail 400x400^ -gravity center -extent 400x400 -define jpeg:extent=700kb /tmp/output.jpg'.format(filename), shell=True)
                    api.update_profile_image('/tmp/output.jpg')
                else:
                    api.update_profile_image(filename)
            except:
                traceback.print_exc()
                return '''
                <!doctype html>
                <html>
                <head>
                <meta charset="utf-8"/>
                <titleアップロードされました</title>
                </head>
                <body>
                <p>原因不明のエラーが起こりました。時間をおいてまた実行してください</p>
                </body>
                </html>
                '''
            return '''
            <!doctype html>
            <html>
            <head>
            <meta charset="utf-8"/>
            <title>アップロードされました</title>
            </head>
            <body>
            <p>アイコンは正常に変更されました。</p>
            </body>
            </html>
            '''
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="utf-8"/>
    <title>kivantium icon changer</title>
    </head>
    <h1>kivantium icon changer</h1>
    <p>画像ファイルをアップロードしてください (JPEG, PNG, GIF, WebP)</p>
    <p>ファイルサイズの上限が10MBになりました（自動で400x400にトリミングされます） (2019/03/04)</p>
    <form method="post" enctype="multipart/form-data" accept="image/*">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
    '''
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=12345)

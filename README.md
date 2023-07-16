まほろ
=========

[@mitra_sun22](https://twitter.com/mitra_sun22)と[@mahoro@mstdn.poyo.me](https://mstdn.poyo.me/@mahoro)のソースコードです。

- `kabu.py`: 毎時0分に実行されます。時報・ドル円・ビットコイン相場を表示します。
- `anime.py`: 20:50, 21:50, 22:50, 23:50に実行されます。[しょぼいカレンダー](http://cal.syoboi.jp/)から取得したTOKYO MXとテレビ東京のアニメ情報を表示します。
- `news.py`: 毎分実行されます。ニュースアカウントをチェックして特定の条件を満たすツイートを引用RTします。Twitter APIキーの有料化により現在は使えません
- `tenki.py`: 05:10, 06:10, 07:10, 08:10, 09:10に実行されます。その日の天気予報画像を生成してツイートします。Twitter APIキーの有料化により現在は使えません
- `tenki_tomorrow.py`: 22:00に実行されます。次の日の天気予報画像を生成してツイートします。Twitter APIキーの有料化により現在は使えません

サーバー設定メモ
----------------
### 定時に走るスクリプト
```
sudo timedatectl set-timezone Asia/Tokyo
sudo service cron restart
sudo apt update
sudo apt install python3-pip python3-opencv
pip3 install beautifulsoup4 feedparser pillow
```

`crontab -e` に以下を記述
```
# m h  dom mon dow   command
0  *  *  *  * /home/ubuntu/mahoro/kabu.py >/dev/null 2>&1
*  *  *  *  * /home/ubuntu/mahoro/news.py >/dev/null 2>&1
50  20-23  *  *  * /home/ubuntu/mahoro/anime.py >/dev/null 2>&1
10  5-9  *  *  * /home/ubuntu/mahoro/tenki.py >/dev/null 2>&1
00  22  *  *  * /home/ubuntu/mahoro/tenki_tomorrow.py >/dev/null 2>&1
```

### サーバーの設定
#### リバースプロキシの設定
`/etc/nginx/sites-available/default`の
```
location / {
        # First attempt to serve request as file, then
        # as directory, then fall back to displaying a 404.
        try_files $uri $uri/ =404;
}
```
の下に以下を追記
```
location /icon/ {
        client_max_body_size 10M;
        proxy_pass http://localhost:12345/;
}
```

サーバースクリプトをnohupで実行しておく
```
nohup python3 server.py >server-log.txt 2>&1 &
```

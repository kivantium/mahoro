#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
// ※※ このコードは「空白４文字」でインデントしてあります ※※
//
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
//_/
//_/  --- Python 移植版 ( Update: 2018/12/8 ) ---
//_/
//_/  CopyRight(C) K.Tsunoda(AddinBox) 2001 All Rights Reserved.
//_/  ( AddinBox  http://addinbox.sakura.ne.jp/index.htm )
//_/  (  旧サイト  http://www.h3.dion.ne.jp/~sakatsu/index.htm )
//_/
//_/  この祝日判定コードは『Excel:kt関数アドイン』で使用しているものです。
//_/  このロジックは、レスポンスを第一義として、可能な限り少ない
//_/  【条件判定の実行】で結果を出せるように設計してあります。
//_/
//_/  この関数では以下の祝日変更までサポートしています。
//_/    (a) 2019年施行の「天皇誕生日の変更」 12/23⇒2/23 (補：2019年には[天皇誕生日]はありません)
//_/    (b) 2019年の徳仁親王の即位日(5/1) および
//_/       祝日に挟まれて「国民の休日」となる 4/30(平成天皇の退位日) ＆ 5/2 の２休日
//_/    (c) 2019年の「即位の礼 正殿の儀 (10/22) 」
//_/    (d) 2020年施行の「体育の日の改名」⇒スポーツの日
//_/    (e) 五輪特措法による2020年の「祝日移動」 
//_/       海の日：7/20(3rd Mon)⇒7/23, スポーツの日:10/12(2nd Mon)⇒7/24, 山の日：8/11⇒8/10
//_/
//_/  (*1)このコードを引用するに当たっては、必ずこのコメントも
//_/      一緒に引用する事とします。
//_/  (*2)他サイト上で本マクロを直接引用する事は、ご遠慮願います。
//_/      【 http://addinbox.sakura.ne.jp/holiday_logic.htm 】
//_/      へのリンクによる紹介で対応して下さい。
//_/  (*3)[ktHolidayName]という関数名そのものは、各自の環境に
//_/      おける命名規則に沿って変更しても構いません。
//_/  
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

  追記 SETOGUCHI Mitsuhiro      http://straitmouth.jp/

  * 2007/May/26
  このスクリプトは JavaScript 用判定コード
    http://addinbox.sakura.ne.jp/holiday_logic.htm#JS
  を元に、Python 向けに移植したものです。

  holiday_name() は、年、月、日の3つの整数の引数を取ります。
  不適切な値を与えると、 ValueError が発生します。
  与えた日付が日本において何らかの祝日であれば、その名前が Unicode で返ります。
  祝日でない場合は None が返ります。

  * 2010/Sep/21
  holiday_name() にキーワード引数として datetime.date のオブジェクトも取れる
  ようにしました。これを指定する際は年、月、日は指定する必要がなく、指定しても
  無視されます。これにより、 jholiday モジュールを使用するスクリプトがすでに
  datetime.date のオブジェクトがある場合の効率が若干良くなります。

  holiday_name() は、指定した日が祝日であれば 
    Python 2.x 以前の場合は Unicode 文字列を、 
    Python 3.x 以降の場合は文字列を
  返します。指定した日が祝日でなければ、 Python のバージョンによらず None を返します。

  * 2014/May/29
  [山の日]改正の修正

  * 2015/Nov/30
  [ import math ]の記述をコードの先頭に追記

  * 2018/Feb/15
  [天皇誕生日の変更]改正の修正

  * 2018/June/21
  ５月４日 ( 国民の休日：1986～2006年 ) 及び 振替休日の判定処理に誤りがありましたので修正しました。

  * 2018/June/21
  [体育の日⇒スポーツの日 改名] ＆ [五輪特措法による祝日移動] 改正の修正

  * 2018/July/20
  [ import sys ]の記述が抜けていましたので追記しました

  * 2018/Dec/8
  [即位の日 および 4/30 & 5/2の国民の休日] [即位礼正殿の儀] 改正の修正


サンプル

Python 2.6.1 (r261:67515, Feb 11 2010, 15:47:53) 
[GCC 4.2.1 (Apple Inc. build 5646)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> import jholiday
>>> jholiday.holiday_name(2007, 4, 28)
None
>>> jholiday.holiday_name(2007, 4, 29)
u'\u662d\u548c\u306e\u65e5'
>>> print jholiday.holiday_name(2007, 4, 29).encode('euc-jp')
昭和の日
>>> import datetime
>>> date = datetime.date(2007, 4, 29)
>>> jholiday.holiday_name(date = date)
u'\u662d\u548c\u306e\u65e5'


Python 3.1.2 (r312:79360M, Mar 24 2010, 01:33:18) 
[GCC 4.0.1 (Apple Inc. build 5493)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import jholiday
>>> jholiday.holiday_name(2007, 4, 28)
>>> jholiday.holiday_name(2007, 4, 29)
'昭和の日'
>>> print(jholiday.holiday_name(2007, 4, 29))
昭和の日
>>> import datetime
>>> date = datetime.date(2007, 4, 29)
>>> jholiday.holiday_name(date = date)
'昭和の日'
"""


import datetime
import math
import sys

MONDAY, TUESDAY, WEDNESDAY, SUNDAY = 0, 1, 2, 6    # 月(0), 火(1), 水(2), 木(3), 金(4), 土(5), 日(6)

def _vernal_equinox(y):
    # 整数で年を与えると、その年の春分の日が3月の何日であるかを返す
    if y <= 1947:
        d = 99    # 祝日法施行前
    elif y <= 1979:
        d = math.floor(20.8357  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2099:
        d = math.floor(20.8431  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2150:
        d = math.floor(21.8510  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    else:
        d = 99    # 2151年以降は略算式が無いので不明

    return d

def _autumn_equinox(y):
    # 整数で年を与えると、その年の秋分の日が9月の何日であるかを返す
    if y <= 1947:
        d = 99    # 祝日法施行前
    elif y <= 1979:
        d = math.floor(23.2588  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2099:
        d = math.floor(23.2488  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    elif y <= 2150:
        d = math.floor(24.2488  +  0.242194 * (y - 1980)  -  math.floor((y - 1980) / 4))
    else:
        d = 99    # 2151年以降は略算式が無いので不明

    return d

def holiday_name(year = None, month = None, day = None, date = None):
    # holiday_name() の呼び出し方法は2通りあります。
    #
    # 1つ目の方法は、3つの引数 year, month, day に整数を渡す方法です。
    # もうひとつの方法は前述のキーワード引数 date に datetime.date のオブジェクトを渡す方法です。
    # この場合は year, month, day を渡す必要はなく、また、渡したとしても無視されます。
    #
    # holiday_name() は、その日が祝日であれば 
    #     Python 2.x 系以前の場合には Unicode 文字列で
    #     Python 3.x 系以降の場合には文字列で
    # 祝日名を返します。
    # 指定した日が祝日でなければ、 Python のバージョンによらず None を返します。

    # [ date ]引数が省略された場合は [ year, month, day ]引数で日付を作成し [ date ]引数を差し替える。
    if date == None:
        date = datetime.date(year, month, day)

    if date < datetime.date(1948, 7, 20):
        return None    # 祝日法施行前： None で返す
    else:
        name = None    # name の初期値は None


    #-- １月--
    if date.month == 1:
        if date.day == 1:
            name = '元日'
        else:
            if date.year >= 2000:
                if int((date.day - 1) / 7) == 1 and date.weekday() == MONDAY:    # 2nd Monday
                    name = '成人の日'
            else:
                if date.day == 15:
                    name = '成人の日'
    #-- ２月 --
    elif date.month == 2:
        if date.day == 11 and date.year >= 1967:
            name = '建国記念の日'
        elif date.day == 23 and date.year >= 2020:
            name = '天皇誕生日'
        elif (date.year, date.month, date.day) == (1989, 2, 24):
            name = '昭和天皇の大喪の礼'
    #-- ３月 --
    elif date.month == 3:
        if date.day == _vernal_equinox(date.year):    # 1948～2150以外は[99]が返るので､必ず≠になる
            name = '春分の日'
    #-- ４月 --
    elif date.month == 4:
        if date.day == 29:
            if date.year >= 2007:
                name = '昭和の日'
            elif date.year >= 1989:
                name = 'みどりの日'
            else:
                name = '天皇誕生日'  # 昭和天皇
        elif (date.year, date.month, date.day) == (2019, 4, 30):
            name = '国民の休日'    # 平成天皇の退位日(祝日ではなく「国民の休日」です)
        elif (date.year, date.month, date.day) == (1959, 4, 10):
            name = '皇太子明仁親王の結婚の儀'
    #-- ５月 --
    elif date.month == 5:
        if date.day == 3:
            name = '憲法記念日'
        elif date.day == 4:
            if date.year >= 2007:
                name = 'みどりの日'
            elif (date.year >= 1986) and date.weekday() not in (MONDAY, SUNDAY):  # 火曜 以降(火～土)
                # 5/4が日曜日は『只の日曜』､月曜日は『憲法記念日の振替休日』(～2006年)
                name = '国民の休日'
        elif date.day == 5:
            name = 'こどもの日'
        elif date.day == 6:
            if date.year >= 2007 and date.weekday() in (TUESDAY, WEDNESDAY):  # [5/3,5/4が日曜]ケースのみ、ここで判定
                name = '振替休日'
        else:
            if (date.year, date.month, date.day) == (2019, 5, 1):
                name = '即位の日'    # 徳仁親王
            elif (date.year, date.month, date.day) == (2019, 5, 2):
                name = '国民の休日'    # 祝日ではなく「国民の休日」です
    #-- ６月 --
    elif date.month == 6:
        if (date.year, date.month, date.day) == (1993, 6, 9):
            name = '皇太子徳仁親王の結婚の儀'
    #-- ７月 --
    elif date.month == 7:
        if date.year >= 2021:
            if int((date.day - 1) / 7) == 2 and date.weekday() == MONDAY:    # 3rd Monday
                name = '海の日'
        elif date.year == 2020:
            # 2020年はオリンピック特措法により
            # 「海の日」が 7/23 , 「スポーツの日」が 7/24 に移動
            if date.day == 23:
                name = '海の日'
            elif date.day == 24:
                name = 'スポーツの日'
        elif date.year >= 2003:
            if int((date.day - 1) / 7) == 2 and date.weekday() == MONDAY:    # 3rd Monday
                name = '海の日'
        elif date.year >= 1996:
            if date.day == 20:
                name = '海の日'
    #-- ８月 --
    elif date.month == 8:
        if date.year >= 2021:
            if date.day == 11:
                name = '山の日'
        elif date.year == 2020:
            # 2020年はオリンピック特措法により「山の日」が 8/10 に移動
            if date.day == 10:
                name = '山の日'
        elif date.year >= 2016:
            if date.day == 11:
                name = '山の日'
    #-- ９月 --
    elif date.month == 9:
        autumn_equinox = _autumn_equinox(date.year)
        if date.day == autumn_equinox:    # 1948～2150以外は[99]が返るので､必ず≠になる
            name = '秋分の日'
        else:
            if date.year >= 2003:
                if int((date.day - 1) / 7) == 2 and date.weekday() == MONDAY:    # 3rd Monday
                    name = '敬老の日'
                elif date.weekday() == TUESDAY and date.day == autumn_equinox - 1:
                    name = '国民の休日'    # 火曜日＆[秋分日の前日]
            elif date.year >= 1966 and date.day == 15:
                name = '敬老の日'
    #-- １０月 --
    elif date.month == 10:
        if date.year >= 2021:
            if int((date.day - 1) / 7) == 1 and date.weekday() == MONDAY:    # 2nd Monday
                name = 'スポーツの日'    # 2020年より改名
        elif date.year == 2020:
            # 2020年はオリンピック特措法により「スポーツの日」が 7/24 に移動
            pass
        elif date.year >= 2000:
            if int((date.day - 1) / 7) == 1 and date.weekday() == MONDAY:    # 2nd Monday
                name = '体育の日'
            elif (date.year, date.month, date.day) == (2019, 10, 22):
                name = '即位礼正殿の儀'    # 徳仁親王
        elif date.year >= 1966:
            if date.day == 10:
                name = '体育の日'
    #-- １１月 --
    elif date.month == 11:
        if date.day == 3:
            name = '文化の日'
        elif date.day == 23:
            name = '勤労感謝の日'
        elif (date.year, date.month, date.day) == (1990, 11, 12):
            name = '即位礼正殿の儀'
    #-- １２月 --
    elif date.month == 12:
        if date.day == 23 and date.year >= 1989 and date.year <= 2018:
            name = '天皇誕生日'  # 平成天皇


    # ----- 振替休日の判定 (振替休日施行日:1973/4/12) -----
    # [ 対象日≠祝日/休日 ＆ 対象日＝月曜日 ]のみ、前日(＝日曜日)を祝日判定する。
    # 前日(＝日曜日)が祝日の場合は”振替休日”となる。
    # 尚、５月６日の扱いを
    #     「火曜 or 水曜(みどりの日(5/4) or 憲法記念日(5/3)の振替休日)」⇒５月ブロック内で判定済
    #     「月曜(こどもの日(5/5)の振替休日」⇒ここの判定処理で判定
    # とする事により、ここでの判定対象は『対象日が月曜日』のみ となります。
    #
    # name は祝日名 or None (初期値, 祝日ではない場合の値)です。
    # 論理演算では「空文字以外の文字列⇒true, 空文字⇒false, None⇒false 」と扱われます。
    # [ not name ] は、祝日名が得られた⇒false , 祝日が得られない⇒true となります。
    if (not name) and (date.weekday() == MONDAY) and (date >= datetime.date(1973, 4, 12)):
        prev = date + datetime.timedelta(days = -1)
        if holiday_name(prev.year, prev.month, prev.day):
            name = '振替休日'


    # holiday_name() は 指定した日が祝日であれば
    #     Python 2.x 以前の場合は Unicode 文字列を、
    #     Python 3.x 以降の場合は文字列を
    # 返します。指定した日が祝日でなければ Python のバージョンによらず None を返します。
    if name and sys.version_info[0] < 3:
        name = unicode(name, 'utf-8')

    return name    # [祝日]等：その名称 , 祝日ではない：None


"""
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
//_/ CopyRight(C) K.Tsunoda(AddinBox) 2001 All Rights Reserved.
//_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/
"""




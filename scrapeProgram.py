import requests
from bs4 import BeautifulSoup
import sys
from time import sleep

query = "乃木坂" #検索ワード
url = "https://tv.yahoo.co.jp/search/?q="+query+"&t=1%202%203&a=23&oa=1&s=1" #地上波、BS、CS　地域設定：東京
res = requests.get(url)
status = res.status_code
 
#Requestsのステータスコードが200以外ならばLINEに通知して終了
if status != 200:
    def LineNotify(message):
        line_notify_token = "アクセストークン"
        line_notify_api = "https://notify-api.line.me/api/notify"
        payload = {"message": message}
        headers = {"Authorization": "Bearer " + line_notify_token}
        requests.post(line_notify_api, data=payload, headers=headers)
    message = "アクセスに失敗しました"
    LineNotify(message)
    sys.exit()

#ステータスコードが200ならば処理継続
else:
    pass

#キーワード検索数を取得
soup = BeautifulSoup(res.text,"html.parser")
p = soup.find("p",class_="floatl pt5p")

#検索数が0ならば処理終了
if p == None:
    sys.exit()  #以降の処理には進まず終了

#検索数が1以上ならば処理継続
else:
    pass

answer = int(p.em.text) #検索数
page = 1
list1 = []  #放送日時用リスト
list2 = []  #放送局用リスト
list3 = []  #番組タイトル用リスト

#検索数からページごとに情報取得を繰り返す処理
while answer > 0:
    url = "https://tv.yahoo.co.jp/search/?q="+query+"&t=1%202%203&a=23&oa=1&s="+str(page) #地上波、BS、CS　地域設定：東京
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    dates = soup.find_all("div",class_="leftarea")
    for date in dates:
        d = date.text
        d = ''.join(d.splitlines())
        list1.append(d)

    for s in soup("span",class_="floatl"):
        s.decompose()
    tvs = soup.find_all("span",class_="pr35")
    for tv in tvs:
        list2.append(tv.text)

    titles = soup.find_all("div",class_="rightarea")
    for title in titles:
        t = title.a.text
        list3.append(t)

    page = page + 10
    answer = answer - 10

    sleep(3)

#list1～list3から放送日時＋放送局＋番組タイトルをまとめたlist_newの作成
list_new = [x +" "+ y for (x , y) in zip(list1,list2)]
list_new = [x +" "+ y for (x , y) in zip(list_new,list3)]

#テキストファイルから前回のデータを集合として展開する
f = open('hogehoge.txt','r')    #ファイル読み込み
f_old = f.read()
list_old = f_old.splitlines()   #文字列を改行ごとにリスト化
set_old = set(list_old)         #リストを集合に変換
f.close()                       # ファイルを閉じる

#前回のデータと今回のデータの差集合をとる
set_new = set(list_new)
set_dif = set_new - set_old
 
#差集合がなければ処理終了
if len(set_dif) == 0:
    sys.exit()  #以降の処理には進まず終了
 
#差集合があればリストとして取り出してLINEに通知する
else:
    list_now = list(set_dif)
    list_now.sort()
 
    for L in list_now:
        def LineNotify(message):
            line_notify_token = "アクセストークン"
            line_notify_api = "https://notify-api.line.me/api/notify"
            payload = {"message": message}
            headers = {"Authorization": "Bearer " + line_notify_token}
            requests.post(line_notify_api, data=payload, headers=headers)
        message = "新しい番組情報です\n\n" + L
        LineNotify(message)
        sleep(3)
 
f = open('hogehoge.txt', 'w')   # 書き込みモードで開く
for x in list_new:
    f.write(str(x)+"\n")    #list_newを文字列に変換＆改行してファイル書き込み
f.close()   # ファイルを閉じる
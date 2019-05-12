import requests
from bs4 import BeautifulSoup
import sys
from time import sleep
import datetime

# 定期ジョブにする場合はキーワード決め打ちにする
print('番組検索キーワードを入力してください')
query = input('>> ') #検索ワード
url = "https://tv.yahoo.co.jp/search/?q="+format(query)+"&t=1%202%203&a=23&oa=1&s=1" #地上波、BS、CS　地域設定：東京
res = requests.get(url)
status = res.status_code

# ライン通知メソッド
def LineNotify(message):
    line_notify_token = "アクセストークン"
    line_notify_api = "https://notify-api.line.me/api/notify"
    payload = {"message": message}
    headers = {"Authorization": "Bearer " + line_notify_token}
    requests.post(line_notify_api, data=payload, headers=headers)

# ファイルがなければ空のファイル作成
f = open('program_log.txt', 'a')
f.close

#Requestsのステータスコードが200以外ならばLINEに通知して終了
if status != 200:
    message = "アクセスに失敗しました"
    LineNotify(message)
    # プログラム終了
    sys.exit()
#200ならば処理継続
else:
    pass

#キーワード検索数を取得
soup = BeautifulSoup(res.text,"html.parser")
p = soup.find("p",class_="floatl pt5p")

#検索数が0ならば処理終了
if p == None:
    sys.exit()  #以降の処理には進まず終了
#1以上ならば処理継続
else:
    pass

answer = int(p.em.text) #検索数
# ファイルへのの書き込み用変数に代入
num_answer = answer
print(str(num_answer) + '件の番組がヒットしました')

page = 1          #最初のページ数を指定
datelist = []     #放送日時用リスト
channellist = []  #放送局用リスト
programlist = []  #番組タイトル用リスト

#検索数からページごとに情報取得を繰り返す処理
while answer > 0:
    url = "https://tv.yahoo.co.jp/search/?q="+query+"&t=1%202%203&a=23&oa=1&s="+str(page) #地上波、BS、CS　地域設定：東京
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    dates = soup.find_all("div",class_="leftarea")
    for date in dates:
        d = date.text
        d = ''.join(d.splitlines())
        datelist.append(d)

    for s in soup("span",class_="floatl"):
        s.decompose()
    tvs = soup.find_all("span",class_="pr35")
    for tv in tvs:
        channellist.append(tv.text)

    titles = soup.find_all("div",class_="rightarea")
    for title in titles:
        t = title.a.text
        programlist.append(t)

    page = page + 10
    answer = answer - 10

    # 負荷軽減のため
    # sleep(3)

#datelist～programlistから放送日時＋放送局＋番組タイトルをまとめたlist_newの作成
list_new = [x +" "+ y for (x , y) in zip(datelist,channellist)]
list_new = [x +" "+ y for (x , y) in zip(list_new,programlist)]

#テキストファイルから前回のデータを集合として展開する
f = open('program_log.txt','r')    #ファイル読み込み
f_old = f.read()
list_old = f_old.splitlines()   #文字列を改行ごとにリスト化
set_old = set(list_old)         #リストを集合に変換
f.close()                       # ファイルを閉じる

#前回のデータと今回のデータの差集合をとる
set_new = set(list_new)
set_dif = set_new - set_old

#差集合がなければ処理終了
if len(set_dif) == 0:
    print('新しい番組情報はありませんでした')
    sys.exit()  #以降の処理には進まず終了

#差集合があればリストとして取り出してLINEに通知する
else:
    list_now = list(set_dif)
    list_now.sort()
    nowquantity = len(list_now)
    print('このうち取得済みでない番組' + str(nowquantity) + '件の通知を行います')

    i = 1
    for L in list_now:
        message = "番組情報[キーワード：" + query + "]\n\n" + L
        LineNotify(message)
        #進捗表示(1行に表示される)
        sys.stdout.write('\r' + str(i) + ' / ' + str(nowquantity))
        sys.stdout.flush()
        sleep(0.1)
        i += 1
        # サーバ負荷を軽減するため
        # sleep(3)

f = open('program_log.txt', 'a')   # 書き込みモードで開く
f.write('検索ワード: ' + query + '   ヒット数: ' + str(num_answer) + "\n")
# 実行時間
dt_now = datetime.datetime.now()
f.write('実行日時：')
f.write(dt_now.strftime('%Y年%m月%d日 %H:%M:%S\n'))

for x in list_new:
    f.write(str(x)+"\n")    #list_newを文字列に変換＆改行してファイル書き込み
f.write("\n")
f.close()

print('\n通知が完了しました')
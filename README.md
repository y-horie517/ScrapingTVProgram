# ヤフー番組表の検索結果をLINE通知
コンソールから検索ワードを入力すると、ヒットした番組情報がLINEで通知される。通知先は下記アクセストークン作成時に指定

実行例  
コンソール  
<img width="321" alt="output_console_sample" src="https://user-images.githubusercontent.com/47136469/57586176-1f436780-752d-11e9-95db-fb2549d32dc3.png">  

ログファイル(program_log.txt)   
<img width="632" alt="output_log_sample" src="https://user-images.githubusercontent.com/47136469/57586175-19e61d00-752d-11e9-9f0a-06644b7f13f6.png">  

LINE通知  
![IMG_5430](https://user-images.githubusercontent.com/47136469/57586289-d8567180-752e-11e9-8b7b-1a574e3733d2.PNG)


* Python 3.7.3
* コード内の  
  line_notify_token = "アクセストークン"  
  を取得したトークンで置き換えて実行

* 待機時間を入れると、ヒット数が多い場合処理に時間がかかるため、  
 $ time python scrapeProgram.py  
 などで実行時間を測定

## LINE公式サイトからアクセストークンを取得
*  https://notify-bot.line.me/ja/ にアクセスしログイン
*  マイページ内のトークン発行ボタンからトークン生成し、発行されたトークンをメモする
※トークンの扱いに注意

## ヤフー番組表での検索結果URLについて
例：
https://tv.yahoo.co.jp/search/?q=ニュース&t=1%202%203&a=23&oa=1&s=1

* q: 検索ワード
* a: 地域設定[23: 東京] など
* t: [1:BS, 2:CS, 3:地上波]
* s:　ページ 1ページ目 => 1 2ページ目 => 11 3ページ目 => 21



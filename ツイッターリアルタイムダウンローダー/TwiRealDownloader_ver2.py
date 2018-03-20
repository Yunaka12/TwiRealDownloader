from twython import Twython, TwythonError
from requests_oauthlib import OAuth1Session
import urllib.request
import re
import time
import os
from glob import glob
import datetime
import emoji


print("\n*　*　*　*　*　*　*　*　*　*")
print("TwiRealDownloader ver.2")
print("最終更新:2018/03/20")
print("*　*　*　*　*　*　*　*　*　*\n")
print("監視したいアカウントのユーザーID（@不要）を入力してください。")
userID = input(">>> ")
print("監視中...")
print("監視を続ける場合はこのまま放置してください。")
print("監視を終える場合はこのツールを閉じてください。")

#フォルダの作成
name = userID
path = "./"+name+"さんのフォルダ"
if not os.path.exists(path):
    os.mkdir(path)
os.chdir(path)

#ツイートを書き込むテキストファイル
f = open('Tweets.txt','a')
f.close()

#OAuth2認証
APP_KEY = "" # https://apps.twitter.com/から取得する
APP_SECRET = ""　# https://apps.twitter.com/から取得する
twitter = Twython(APP_KEY, APP_SECRET, oauth_version = 2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

#ツイートから絵文字を除去する関数
def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)

#ツイート日時を成型する関数
def editTime(date):
    date = content["created_at"]
    month_num={"Jan":"1","Feb":"2","Mar":"3","Apr":"4","May":"5","Jun":"6","Jul":"7","Aug":"8","Sep":"9","Oct":"10","Nov":"11","Dec":"12"}
    twi_year=date[26:30]
    twi_month=month_num[date[4:7]]
    twi_day = date[8:10]
    twi_time = int(date[11:13])
    twi_time = twi_time+9
    twi_time = str(twi_time)+date[13:16]
    return twi_year+"/"+twi_month+"/"+twi_day+" "+twi_time

#ツイートを取得する関数
def getTL():
    #最新のツイートを1件取得
    global content,twi_when
    timeline = twitter.get_user_timeline(screen_name=userID, count=1,include_entities="True",
    exclude_replies="False",include_rts="False")
    content = timeline[0]
    twi_when = editTime(content["created_at"])

#メディアをダウンロードする関数
def getContents():
    #メディア付きツイートの場合
    if "extended_entities" in content:
        check = content["extended_entities"]["media"][0]["type"]
        searched_file = glob("Twi*")
        try:
            #ファイル名の設定
            if len(searched_file) > 0:
                max_file =searched_file[len(searched_file)-1]
                number_file = max(list(map(lambda s:int(re.search("[0-9]+",s).group(0)),searched_file)))
                number_file = number_file + 1
                new_file = "Twi"+str(number_file)
            else:
                new_file = "Twi1"
            #メディアのダウンロード
            if check == "video" or check == "animated_gif": #動画とgif
                gif_url = content["extended_entities"]["media"][0]["video_info"]["variants"][0]["url"]
                urllib.request.urlretrieve(gif_url,new_file+".mp4") #動画もgifも拡張子はmp4で保存

            elif check == "photo": #画像
                title =["a","b","c","d"]
                for i in range(0,len(content["extended_entities"]["media"]),1):
                    image_url = content["extended_entities"]["media"][i]["media_url"]
                    urllib.request.urlretrieve(image_url,new_file+"_"+title[i]+".jpg") #複数枚対応
        except:
            pass
    else:
        pass

#メインの処理
first =0
while True:
    if first==0:
        getTL()
        getContents()
        oldTwit = content["text"]
        try:
            f = open('Tweets.txt','a')
            f.write(remove_emoji(oldTwit)+" "+"ツイート日時"+twi_when+"\n")
            f.close()
        except:
            f = open('Tweets.txt','a')
            f.write("ツイートの取得に失敗"+" "+"ツイート日時"+twi_when+"\n")
            f.close()
        first += 1
        time.sleep(3)
    elif first==1:
        getTL()
        newTwit = content["text"]
        if oldTwit != newTwit:
            first += 1
            try:
                f = open('Tweets.txt','a')
                f.write(remove_emoji(newTwit)+" "+"ツイート日時"+twi_when+"\n")
                f.close()
            except:
                f = open('Tweets.txt','a')
                f.write("ツイートの取得に失敗"+" "+"ツイート日時"+twi_when+"\n")
                f.close()
        elif oldTwit == newTwit:
            first = 1
        time.sleep(3)
    elif first==2:
        getContents()
        oldTwit = content["text"]
        first -= 1
        time.sleep(3)

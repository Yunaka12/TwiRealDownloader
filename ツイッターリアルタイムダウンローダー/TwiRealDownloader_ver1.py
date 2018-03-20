from twython import Twython, TwythonError
from requests_oauthlib import OAuth1Session
from datetime import datetime
import urllib.request
import re
import random
import time
import os

APP_KEY = "7GDTlipks1O6i1gZgJyzAIq6T"
APP_SECRET = "OPAzarDM8Goel2TLMiQ0UdsDDA0XHm4XnFMsCtomATMVj3t7Mn"

# OAuth2(AccessTokenの取得)
twitter = Twython(APP_KEY, APP_SECRET, oauth_version = 2)
ACCESS_TOKEN = twitter.obtain_access_token()
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

username = os.getlogin()
folder = r".\RealtimeTwiDownloads"
if not os.path.exists(folder):
    os.mkdir(folder)

print("\n*　*　*　*　*　*　*　*　*　*")
print("TwiRealDownloader ver.1\n")
print("このツールの使用はすべて自己責任で行ってください。")
print("このツールが保存するデータはツール起動以降に投稿された画像/動画です。")
print("データはダウンロードフォルダ内のTwiDownloadsフォルダに保存されます。")
print("このツールを閉じるときは右上の×をクリックしてください。")
print("最終更新:2018/02/05")
print("*　*　*　*　*　*　*　*　*　*\n")
print("監視したいアカウントのユーザーID（@不要）を入力してください。")
userId = input(">>> ")

def getTL():
    global req, timeline, content
    timeline = twitter.get_user_timeline(screen_name=userId, count=1,include_entities="True",
    exclude_replies="True",include_rts="False")
    content = timeline[0]

def getContents():
    if "extended_entities" in content: #extended_entitiesがある→画像か動画付きツイート
        content_check = content["extended_entities"]["media"][0]
        if "video_info" in content_check:
            video_url = content["extended_entities"]["media"][0]["video_info"]["variants"][1]["url"]
            nowtime = str(datetime.now())
            time_modify1 = re.sub("-|:| ", "", nowtime)
            time_modify2 = time_modify1[:12]+"R"+str(random.randint(1,1000))
            title = time_modify2+".mp4" #動画はすべてmp4で保存
            fn = r".\RealtimeTwiDownloads\%s" % (title)
            urllib.request.urlretrieve(video_url,fn)
            contents = content["text"]+"\n"+nowtime[:16]+"\n"
            print(contents)

        else: #動画が含まれていないのにextended_entitiesがある→画像がある
            for i in range(len(content["extended_entities"]["media"])):
                image_url = content["extended_entities"]["media"][i]["media_url"]
                nowtime = str(datetime.now())
                time_modify1 = re.sub("-|:| ", "", nowtime)
                time_modify2 = time_modify1[:12]+"R"+str(random.randint(1,1000))
                title = time_modify2+".jpeg" #画像はすべてjpegで保存
                fn = r".\RealtimeTwiDownloads\%s" % (title)
                urllib.request.urlretrieve(image_url,fn)
                contents = content["text"]+"\n"+nowtime[:16]+"\n"
            print(contents)

    else:
        nowtime = str(datetime.now())
        contents = content["text"]+"\n"+nowtime[:16]+"\n"
        print("\n"+contents)

first =0
while True:
    try:
        if first==0:
            getTL()
            getContents()
            oldTwit = timeline[0]["text"]
            first += 1
        elif first==1:
            getTL()
            newTwit = timeline[0]["text"]
            if oldTwit != newTwit:
                first += 1
            elif oldTwit == newTwit:
                first = 1
        elif first==2:
            getContents()
            oldTwit = timeline[0]["text"]
            first -= 1
        time.sleep(30)
    except:
        print("何らかのエラーが発生しました。")
        time.sleep(1)

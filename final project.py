#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#安裝所需的api
get_ipython().system('pip install --upgrade google-api-python-client')
get_ipython().system('pip install --upgrade google-auth-oauthlib google-auth-httplib2')


# In[1]:


import requests
import os
import re
from googleapiclient.discovery import build
S = requests.Session()#發送請求之後將cookie儲存在session中

URL = "https://bulbapedia.bulbagarden.net/w/api.php"
print("This program's intention is to tell you the effects of different Pokemon types.")#說明此程式的用途
print("It will recommend you 3 Youtube videos about the type after you enter the one you want to know.")
print("The 18 types: Normal, Fighting, Poison, Ground, Flying, Bug, Rock, Ghost, Steel, Fire, Water, Electric, Grass, Ice, Psychic, Dragon, Dark, Fairy.")
while True:
    word = input("Enter a pokemon type:")
    word = word.lower()#以防輸入者輸入為大寫，將輸入內容全部轉為小寫
    if word not in {"normal","fighting","poison","ground","flying","bug","rock","ghost","steel","fire","water","electric","grass","ice","psychic","dragon","dark","fairy"}:
        print("Please check again the spelling !")#若輸入錯誤訊息，提示輸入者檢查拼字後重新輸入
        continue
    else:
        break

PARAMS = {
    'action':"opensearch",#獲得特定關鍵字的簡短介紹
    'search':word,#搜尋關鍵字
    'limit': 5,#返回5個結果
    'namespace':0,#頁面種類為主條目
    'format':"json"#預設回傳json
}

if word in {"fairy"}:#由於不同種類及年代的關係，資料也有所更新，為了得到最新的資料而重新設置一個參數
    q = 0
elif word in {"dragon","fighting","fire","poison","steel","bug"}:
    q = 6
else:
    q = 3

R = S.get(url = URL, params = PARAMS)
DATA = R.json()#將請求的資料轉為json格式
ini = DATA[3][0]

if ini.endswith(")"):#前往type的頁面
    a = ini
else:
    a = (ini + "_(type)")#加工後前往type的頁面

from bs4 import BeautifulSoup

r = requests.get(a)#解析網頁
if r.status_code == requests.codes.ok:#判斷伺服器連線是否正常
    soup = BeautifulSoup(r.text, 'html.parser')#得到soup

ans = soup.find_all("tr", align = "center")#找到align屬性，值為center的內容

#攻擊方面
print("Attack(攻擊):")

#攻擊有利
print("  Super effective(效果絕佳):")
double = ans[q].find("td")
n = 0
dou = double.find_all("a")#找到項目
Se = list()
for n in range(len(dou)):#建立迴圈
    num = re.findall('title="([a-zA-Z]+)',str(dou[n]))#找到攻擊有利的type
    Se.append(num)#將它們加入list之中
    n += 1
if len(Se) < 1:#若沒有找到任何結果
    print("    Nothing")
else:#顯示找到的type
    print("   ",Se)

#攻擊持平
print("  Not very effective(效果不太好):")
double = ans[q+1].find("td")
n = 0
dou = double.find_all("a")#找到項目
Se = list()
for n in range(len(dou)):#建立迴圈
    num = re.findall('title="([a-zA-Z]+)',str(dou[n]))#找到攻擊持平的type
    Se.append(num)#將它們加入list之中
    n += 1
if len(Se) < 1:#若沒有找到任何結果
    print("    Nothing")
else:#顯示找到的type
    print("   ",Se)

#攻擊不奏效
print("  No effective(沒有效果):")
double = ans[q+2].find("td")
n = 0
dou = double.find_all("a")#找到項目
Se = list()
for n in range(len(dou)):#建立迴圈
    num = re.findall('title="([a-zA-Z]+)',str(dou[n]))#找到攻擊不奏效的type
    Se.append(num)#將它們加入list之中
    n += 1
if len(Se) < 1:#若沒有找到任何結果
    print("    Nothing")
else:#顯示找到的type
    print("   ",Se)

#防禦方面
print("Defense(防禦):")

#防禦對方有利
print("  Make no hurt(無法造成傷害):")
double = ans[q+2].find_all("td")[1]
n = 0
dou = double.find_all("a")#找到項目
Se = list()
for n in range(len(dou)):#建立迴圈
    num = re.findall('title="([a-zA-Z]+)',str(dou[n]))#找到防禦對方有利的type
    Se.append(num)#將它們加入list之中
    n += 1
if len(Se) < 1:#若沒有找到任何結果
    print("    Nothing")
else:#顯示找到的type
    print("   ",Se)

#防禦持平
print("  Great resistant(抵抗力強):")
double = ans[q].find_all("td")[1]
n = 0
dou = double.find_all("a")#找到項目
Se = list()
for n in range(len(dou)):#建立迴圈
    num = re.findall('title="([a-zA-Z]+)',str(dou[n]))#找到防禦持平的type
    Se.append(num)#將它們加入list之中
    n += 1
if len(Se) < 1:#若沒有找到任何結果
    print("    Nothing")
else:#顯示找到的type
    print("   ",Se)

#防禦不利
print("  Weekness(弱點):")
double = ans[q+1].find_all("td")[1]
n = 0
dou = double.find_all("a")#找到項目
Se = list()
for n in range(len(dou)):#建立迴圈
    num=re.findall('title="([a-zA-Z]+)',str(dou[n]))#找到防禦不利的type
    Se.append(num)#將它們加入list之中
    n += 1
if len(Se) < 1:#若沒有找到任何結果
    print("    Nothing")
else:#顯示找到的type
    print("   ",Se)
    

#尋找youtube影片

DEVELOPER_KEY = 'AIzaSyCNMFBYfBOaUPf58Znk-swaQ7ZZiZJ-25k'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

#取得數據
def build_resource(properties):#根據properties(key-value pairs)的list建立一個resource
    resource = {}
    for p in properties:#例如將"snippet.title"分成"snippet"和"title","snippet"為object、"title"則是property
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):#建立迴圈
            is_array = False#先將值設成false
            key = prop_array[pa]

            if key[-2:] == '[]':#若properties是array的類型，要將名字轉換(snippet.tags[]轉成snippet.tags)並設立flag來處理值
                key = key[0:len(key)-2:]
                is_array = True

            if pa == (len(prop_array) - 1):
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')#取得需要的部分
                    else:
                        ref[key] = properties[p]#取得需要的部分
            elif key not in ref:#還不具有snippet的項目，要先建立一個
                ref[key] = {}
                ref = ref[key]#下次進行迴圈時，設定property在resource的snippet項目中
            else:#已經有snippet的項目
                ref = ref[key]
    return resource


def remove_empty_kwargs(**kwargs):#移除未設定的keyword arguments
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs

def search_list_by_keyword(client, **kwargs):#搜尋關鍵字
    kwargs = remove_empty_kwargs(**kwargs)
    response = client.search().list(**kwargs).execute()

    return response

print("Here are the videos about Pokemon type "+word+" :")
if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'#設置環境變數防止發生錯誤
    client = build(API_SERVICE_NAME, API_VERSION,developerKey=DEVELOPER_KEY)
  
    resp=search_list_by_keyword(client, part='snippet', maxResults=3, q="pokemon type"+word, type='youtube#video')#找到最受歡迎的前三個影片
    for a in range(0,3):      
        r1=resp['items']#拿到搜索的item
        k1=r1[a]['id']['kind']#取得類型
        if k1 in {'youtube#video'}:#若是影片
            ID = 'videoId'
            v1=(r1[a]['id'][ID])
            print("https://www.youtube.com/watch?v=" + v1)#顯示網址
        else:#若是播放清單
            ID = 'playlistId'
            u1 = r1[a]['snippet']['thumbnails']['default']['url'].split('/')[4]
            v1=(r1[a]['id'][ID])
            print("https://www.youtube.com/watch?v="+u1+'&list='+u1+'&start_radio='+ v1 )#顯示第一個影片的網址


# In[ ]:





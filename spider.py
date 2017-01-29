import requests
from bs4 import BeautifulSoup
import threading
import os
import shutil
import urllib
import re
import random
import codecs
import json
import string

def get_joke():
    url = 'http://www.qiushibaike.com/'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    web = requests.get(url, headers=headers)
    soup = BeautifulSoup(web.text, 'lxml')
    joke = random.choice(soup.select('div.content > span')).get_text()
    return joke

def get_news():
    url = 'http://www.toutiao.com/api/pc/focus/'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    web = requests.get(url, headers=headers)
    data = json.loads(web.text)
    news = ''
    for i in data['data']['pc_feed_focus']:
        news += '· ' + i['title'] + '\n'
    news += '注：新闻均来自今日头条(toutiao.com)'
    return news

def get_hot():
    url = 'http://www.toutiao.com/hot_words/'
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    web = requests.get(url, headers=headers)
    data = json.loads(web.text)
    hots = ''
    for i in data:
        hots += '· {}\n'.format(i)
    hots += '注：热点均来自今日头条(toutiao.com)'
    return hots

def get_tieba_img(url):
    while True:
        dirName = ''.join([random.choice(string.ascii_uppercase) for i in range(8)])
        try:
            os.mkdir(dirName)
            os.chdir(dirName)
            break
        except FileExistsError:
            pass
    count = 0
    crawlUrl = url + '?see_lz=1&pn=1'
    web = requests.get(crawlUrl)
    soup = BeautifulSoup(web.text, 'lxml')
    for img in soup.select('img.BDE_Image'):
        src = img.get('src')
        bigSrc = 'http://imgsrc.baidu.com/forum/pic/item/' + str(src).split('/')[6]
        try:
            req = requests.get(bigSrc, timeout=15, stream=True)
            if req.status_code == 200:
                with open('{}.jpg'.format(count),'wb') as imgFile:
                    req.raw.decode_content = True
                    shutil.copyfileobj(req.raw, imgFile)
            else:
                print('Error while requesting image: {}'.format(bigSrc))
        except Exception:
            print('Timeout while trying to download image: {}'.format(bigSrc))
        count += 1
    return dirName, count

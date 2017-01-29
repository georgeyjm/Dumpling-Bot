#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import itchat
from itchat.content import *
from random import choice
import time
import os
import re
import shutil
import spider, pymath # 我的一些功能

GREETINGS = ('嘿','哟','你好啊','你好呀',':)')
DONT_UNDERSTAND = ('对不起我不明白诶……','抱歉我没听懂:(','不好意思没明白','Sorry没有听懂')
HELP = '我现在虽然聊天不太行，只能打打招呼，但是我可以报时，帮你搜集新闻和热点，甚至还可以讲笑话。我还会求数列的公式！'
WEEKDAYS = {'0':'天','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六'}

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    # msg['Text'](msg['FileName'])
    itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', 'test.png'), msg['FromUserName'])
    return '%s received'%msg['Type']

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.get('isAt') or '@饺子机器人\u2005' in msg['Content']: # 如果@了我
        cont = msg['Content'].replace('@熏鱼饺子\u2005','').replace('@饺子机器人\u2005','')
        print(cont)
        if '帮助' in cont or ('你' in cont and '除了' in cont and '还' in cont) or ('你' in cont and ('会' in cont or '能' in cont) and ('干' in cont or '做' in cont)):
            itchat.send('@{}\u2005{}'.format(msg['ActualNickName'], HELP), msg['FromUserName'])
        elif '几点' in cont or ('现在' in cont and '时间' in cont):
            itchat.send('@{}\u2005现在是{}'.format(msg['ActualNickName'], time.strftime('%Y{}%m{}%d{}{}{} %H:%M:%S').format('年','月','日','星期',WEEKDAYS[time.strftime('%w')])), msg['FromUserName'])
        elif '笑话' in cont and ('讲' in cont or '说' in cont):
            itchat.send('@{}\u2005你等下哈，我编一个……'.format(msg['ActualNickName']), msg['FromUserName'])
            itchat.send('@{}\u2005{}'.format(msg['ActualNickName'], spider.get_joke()), msg['FromUserName'])
        elif '新闻' in cont:
            itchat.send('@{}\u2005好，稍等一下'.format(msg['ActualNickName']), msg['FromUserName'])
            itchat.send('@{}\u2005\n{}'.format(msg['ActualNickName'], spider.get_news()), msg['FromUserName'])
        elif '热点' in cont:
            itchat.send('@{}\u2005好，稍等一下'.format(msg['ActualNickName']), msg['FromUserName'])
            itchat.send('@{}\u2005\n{}'.format(msg['ActualNickName'], spider.get_hot()), msg['FromUserName'])
        elif '说' in cont:
            words = '说'.join(cont.split('说')[1:]).strip()
            print(words)
            itchat.send('{}'.format(words), msg['FromUserName'])
        elif cont[:3] == '求数列':
            inp = cont[3:]
            if cont[3] in (' ','：',':'):
                inp = cont[4:]
            inp = inp.replace('，',',')
            try:
                seq = pymath.Sequence(inp)
                itchat.send('@{}\u2005公式是：An = {}'.format(msg['ActualNickName'], seq.generateFormula()), msg['FromUserName'])
            except Exception:
                itchat.send('@{}\u2005这个……你的数列好像出了点毛病？'.format(msg['ActualNickName']), msg['FromUserName'])
        elif cont[:4] == '贴吧图片':
            itchat.send('@{}\u2005稍等一下哈，我收集一下图片！'.format(msg['ActualNickName']), msg['FromUserName'])
            inp = cont[5:]
            urlRe = re.compile(r'(http://)?tieba\.baidu\.com/p/[0-9]+')
            if urlRe.findall(inp):
                if inp[:6] != 'http://':
                    inp = 'http://' + inp
                if '?' in inp:
                    inp = urlRe.search(inp).group()
                dirName, imgCount = spider.get_tieba_img(inp+'/')
                for i in range(imgCount):
                    itchat.send('@img@{}'.format('{}.jpg'.format(i)), msg['FromUserName'])
            itchat.send('@{}\u2005你只能爬取第一页楼主发的图片，要爬取更多图片，请联系@熏鱼饺子\u2005进行账户升级'.format(msg['ActualNickName']), msg['FromUserName'])
            os.chdir('..')
            shutil.rmtree(dirName)
        else:
            for i in ('嘿','你好','hi','hello','hey','bonjour','bonsoir'):
                if i in cont.lower():
                    itchat.send('@{}\u2005{}'.format(msg['ActualNickName'], choice(GREETINGS)), msg['FromUserName'])
                    break
            else:
                itchat.send('@{}\u2005{}'.format(msg['ActualNickName'], choice(DONT_UNDERSTAND)), msg['FromUserName'])

itchat.auto_login(True, enableCmdQR=2)
itchat.run(debug=True)

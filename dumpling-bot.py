#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import itchat
from itchat.content import *
from random import choice
import spider, pymath # 我的一些功能

GREETINGS = ('嘿','哟','你好啊','你好呀',':)')
DONT_UNDERSTAND = ('对不起我不明白诶……','抱歉我没听懂:(','不好意思没明白','Sorry没有听懂')

##@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
##def download_files(msg):
##    msg['Text'](msg['FileName'])
##    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.get('isAt') or '@饺子机器人\u2005' in msg['Content']: # 如果@了我
        cont = msg['Content'].replace('@熏鱼饺子\u2005','').replace('@饺子机器人\u2005','')
        if '笑话' in cont and ('讲' in cont or '说' in cont):
            itchat.send('@{}\u2005你等下哈，我编一个……'.format(msg['ActualNickName']), msg['FromUserName'])
            itchat.send('@{}\u2005{}'.format(msg['ActualNickName'], spider.get_joke()), msg['FromUserName'])
        elif '新闻' in cont:
            itchat.send('@{}\u2005好，稍等一下'.format(msg['ActualNickName']), msg['FromUserName'])
            itchat.send('@{}\u2005\n{}'.format(msg['ActualNickName'], spider.get_news()), msg['FromUserName'])
        elif '热点' in cont:
            itchat.send('@{}\u2005好，稍等一下'.format(msg['ActualNickName']), msg['FromUserName'])
            itchat.send('@{}\u2005\n{}'.format(msg['ActualNickName'], spider.get_hot()), msg['FromUserName'])
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
        else:
            for i in ('嘿','你好','hi','hello','hey','bonjour','bonsoir'):
                if i in cont.lower():
                    itchat.send('@{}\u2005{}'.format(msg['ActualNickName'], choice(GREETINGS)), msg['FromUserName'])
                    break
            else:
                itchat.send('@{}\u2005{}'.format(msg['ActualNickName'], choice(DONT_UNDERSTAND)), msg['FromUserName'])

itchat.auto_login(True, enableCmdQR=2)
itchat.run()

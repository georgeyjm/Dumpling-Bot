import itchat
from random import choice
import time
import os
import re
import shutil
from packages import spider, pymath, zhconvert # 我的一些功能

itchat.auto_login(hotReload=True, enableCmdQR=2) # 登录用户账号以便获取昵称

USERNAME = itchat.search_friends()['NickName'] # 获取自己的昵称
GREETINGS = ('嘿','嗨，我是饺子机器人，有何吩咐？','哟','你好啊','你好呀',':)')
DONT_UNDERSTAND = ('对不起我不明白诶……','抱歉我没听懂:(','不好意思没明白','Sorry没有听懂')
HELP = '我是一个功能性机器人哦，聊天不太行，但是可以干很多事！'
WEEKDAYS = {'0':'天','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六'}

def parse_msg(msg):
    atName = '@' + msg['ActualNickName'] + '\u2005'
    recipient = msg['FromUserName']
    content = msg['Content'].replace('@{}\u2005'.format(USERNAME),'').replace('@{} '.format(USERNAME),'').strip()
    if content[:3] == '求数列':
        inp = content[3:].strip(' :：').replace('，',',').replace(' ','')
        try:
            seq = pymath.Sequence(inp)
            itchat.send('{}公式是：An = {}'.format(atName, seq.generateFormula()), recipient)
        except Exception as e:
            print('[ERROR] 求数列({}) -> {}'.format(inp, e))
            itchat.send('{}额……你的数列好像出了点毛病'.format(atName), recipient)
    elif content[:3] in ('转繁体', '轉繁體'):
        original = content[3:].strip()
        itchat.send('{}繁体文字是：{}'.format(atName, zhconvert.toTraditional(original)), recipient)
    elif content[:3] in ('转简体', '轉簡體'):
        original = content[3:].strip()
        itchat.send('{}简体文字是：{}'.format(atName, zhconvert.toSimplified(original)), recipient)
    elif content[:4] == '贴吧图片':
        itchat.send('{}稍等一下哈，我收集一下图片！'.format(atName), recipient)
        inp = content[5:]
        urlRe = re.compile(r'(http://)?tieba\.baidu\.com/p/[0-9]+')
        if urlRe.findall(inp):
            if inp[:7] != 'http://':
                inp = 'http://' + inp
            if '?' in inp:
                inp = urlRe.search(inp).group()
            # dirName, imgCount = spider.get_tieba_img(inp+'/')
            # for i in range(imgCount):
            #     itchat.send('@img@{}'.format('{}.jpg'.format(i)), msg['FromUserName'])
            title = spider.get_tieba_img(inp + '/')
            itchat.send('@fil@{}.zip'.format(title), recipient)
        itchat.send('{}你只能爬取第一页楼主发的图片，要爬取更多图片，请联系@熏鱼饺子\u2005进行账户升级'.format(atName), recipient)
        time.sleep(5)
        os.remove(title + '.zip')
        shutil.rmtree(title)
    elif content[:4] == '贴吧文字':
        itchat.send('{}稍等一下哈，我整合一下！'.format(atName), recipient)
        inp = content[5:]
        urlRe = re.compile(r'(http://)?tieba\.baidu\.com/p/[0-9]+')
        if urlRe.findall(inp):
            if inp[:7] != 'http://':
                inp = 'http://' + inp
            if '?' in inp:
                inp = urlRe.search(inp).group()
            title = spider.get_tieba_text(inp + '/')
            itchat.send('@fil@{}'.format(title), recipient)
        itchat.send('{}你只能爬取第一页楼主发的文字，要爬取更多内容，请联系@熏鱼饺子\u2005进行账户升级'.format(atName), recipient)
        time.sleep(5)
        os.remove(title)
    elif '帮助' in content or ('你' in content and '除了' in content and '还' in content) or ('你' in content and ('会' in content or '能' in content) and ('干' in content or '做' in content)):
        itchat.send('{}{}'.format(atName, HELP), recipient)
    elif '几点' in content or ('现在' in content and '时间' in content):
        currentTime = time.strftime('%Y{}%m{}%d{}{}{} %H:%M:%S').format('年','月','日','星期',WEEKDAYS[time.strftime('%w')])
        itchat.send('{}现在是{}'.format(atName, currentTime), recipient)
    elif '笑话' in content and ('讲' in content or '说' in content):
        itchat.send('{}你等下哈，我编一个……'.format(atName), recipient)
        itchat.send('{}{}'.format(atName, spider.get_joke()), recipient)
    elif '新闻' in content:
        itchat.send('{}好，稍等一下'.format(atName), recipient)
        itchat.send('{}\n{}'.format(atName, spider.get_news()), recipient)
    elif '热点' in content:
        itchat.send('{}好，稍等一下'.format(atName), recipient)
        itchat.send('{}\n{}'.format(atName, spider.get_hot()), recipient)
    elif '说' in content:
        words = '说'.join(content.split('说')[1:]).strip()
        itchat.send('{}'.format(words), recipient)
    else:
        for i in ('嘿','你好','嗨','hi','hello','hey','bonjour','bonsoir'):
            if i in content.lower():
                itchat.send('{}{}'.format(atName, choice(GREETINGS)), msg['FromUserName'])
                break
        else:
            itchat.send('{}{}'.format(atName, choice(DONT_UNDERSTAND)), msg['FromUserName'])

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    # msg['Text'](msg['FileName'])
    itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', 'test.png'), msg['FromUserName'])
    return '%s received'%msg['Type']

@itchat.msg_register('Text', isGroupChat=True)
def text_reply(msg):
    if msg.get('isAt') or '@{}'.format(USERNAME) in msg['Content'] or '@{} '.format(USERNAME) in msg['Content']: # 如果@了我
        parse_msg(msg)

@itchat.msg_register('Recording', isGroupChat=True)
def recording_reply(msg):
    fileName = msg['FileName']
    msg['Text'](fileName)

itchat.run()

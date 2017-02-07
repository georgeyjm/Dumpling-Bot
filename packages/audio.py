import pydub
import os
import requests
import json
import wave
import base64
import random
import string
from uuid import UUID, getnode

from . import core

def _get_access_token():
    apiKey = 'fRmBHMSpnHwOqnRYmMIeFNNQ'
    secretKey = 'r19EnzuawXpsQy9dwWCfcDhVB9Brv9xi'
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(apiKey, secretKey)
    req = requests.post(url)
    data = json.loads(req.text)
    if data.get('error'):
        core.log('ERROR', 'Get Baidu Access Token -> {}'.format(data.get('error_description')))
        return -1
    else:
        return data.get('access_token')

def recognize(fileName) -> str:
    '''调用百度语音识别API并返回识别出可能性最大的文字数据'''
    fileName = fileName.strip()
    extension = fileName.split('.')[-1].lower()
    if extension == 'mp3':
        try:
            recording = pydub.AudioSegment.from_mp3(fileName) # 打开MP3文件
        except FileNotFoundError: # 文件不存在
            core.log('ERROR', 'Audio File Not Found -> {}'.format(fileName))
            return -1
        os.remove(fileName) # 删除MP3文件
        fileName = fileName[:-3] + 'wav'
        recording.export(fileName, format='wav') # 导出至WAV
    elif extension != 'wav':
        core.log('ERROR', 'Audio format not supported -> {}'.format(extension))
        return -1
    try:
        wavFile = wave.open(fileName, 'rb') # 打开WAV文件
    except FileNotFoundError:
        core.log('ERROR', 'Audio File Not Found -> {}'.format(fileName))
        return -1
    nframes = wavFile.getnframes()
    frameRate = wavFile.getframerate()
    if nframes == 1 or frameRate not in (8000, 16000):
        core.log('ERROR', 'Invalid WAV file -> {}, {}'.format(nframes, frameRate))
        return -1
    audioData = wavFile.readframes(nframes) # 音频数据
    data = { # POST数据
    'format': 'wav',
    'rate': frameRate,
    'channel': 1,
    'cuid': _macAddr,
    'token': _accessToken,
    'len': len(audioData),
    'speech': base64.b64encode(audioData).decode('utf-8') # Base64编码的音频数据
    }
    url = 'http://vop.baidu.com/server_api/'
    req = requests.post(url, json=data) # 发送POST请求，必须使用json，不能使用data
    data = json.loads(req.text) # 将返回数据转换为JSON格式
    if data.get('err_no'): # 请求出错
        core.log('ERROR', 'Posting Audio Data -> {} {}'.format(data['err_no'], data['err_msg']))
        return -1
    os.remove(fileName)
    return data['result'][0]

def generate(text: str, speed=5, pitch=5, volume=5, voice=1):
    '''调用百度语音合成API并返回语音MP3文件地址'''
    data = { # POST数据
    'tex': text,
    'lan': 'zh',
    'tok': _accessToken,
    'ctp': '1',
    'cuid': _macAddr,
    'spd': speed, # 语速，取值0-9，默认为5中语速
    'pit': pitch, # 音调，取值0-9，默认为5中语调
    'vol': volume, # 音量，取值0-9，默认为5中音量
    'per': voice # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女声
    }
    url = 'http://tsn.baidu.com/text2audio/'
    req = requests.post(url, data=data) # 发送POST请求
    audioName = ''.join([random.choice(string.ascii_uppercase) for i in range(8)]) + '.mp3'
    with open(_curdir + audioName, 'wb') as audioFile:
        audioFile.write(req.content)
    return _curdir + audioName

_accessToken = _get_access_token()
_macAddr = '-'.join([UUID(int=getnode()).hex[-12:].upper()[i:i+2] for i in range(0,11,2)])
_curdir = os.path.dirname(os.path.abspath(__file__)) + '/tmp/'
# print(recognize(generate('于佳铭是个制造饺子机器人的人')))

import requests

_url = 'http://opencc.byvoid.com/convert/'

def toTraditional(text):
    # if len(text) > 100:
    req = requests.post(_url, data={'text':text,'config':'s2t.json','precise':'0'})
    return req.text
    # else:
    #     result = ''
    #     for segment in [text[i:i+1000] for i in range(0, len(text), 1000)]:
    #         req = requests.post(_url, data={'text':segment,'config':'s2t.json','precise':'0'})
    #         result += req.text
    #     return result

def toSimplified(text):
    req = requests.post(_url, data={'text':text,'config':'t2s.json','precise':'0'})
    return req.text

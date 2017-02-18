# id (str) - 用户唯一ID，识别用
# level (int) - 用户等级
#   0 - 黑名单(?)
#   1 - 普通用户
#   2 - 升级用户
#   3 - 高级用户(?)

import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__))) # 变更工作目录至当前文件位置

from . import core

_DATA_FILE = 'users.json'
_ALL_LEVELS = (1, 2)

def _user(userId):
    '''Returns the user dic and the index'''
    if not exist(userId):
        core.log('ERROR', 'Locating non-existing user -> {}'.format(userId))
        return -1, -1
    for index, usr in enumerate(data):
        if usr['id'] == userId:
            return usr, index

def _write_data():
    with open(_DATA_FILE, 'w') as dataFile:
        json.dump(data, dataFile, indent=2, sort_keys=True)

def exist(userId):
    for usr in data:
        if usr['id'] == userId:
            return True
    return False

def add(userId, level=1):
    if exist(userId):
        core.log('ERROR', 'Adding existing user -> {}'.format(userId))
        return -1
    data.append({'id': userId, 'level': level})
    _write_data()

def remove(userId):
    if not exist(userId):
        core.log('ERROR', 'Removing non-existing user -> {}'.format(userId))
        return -1
    data.remove(_user(userId)[0])
    _write_data()

def get_level(userId):
    user, index = _user(userId)
    if user != -1:
        return data[index]['level']
    else:
        core.log('ERROR', 'Invalid getting level -> {}'.format(userId))
        return -1

def change_level(userId, newLevel):
    user, index = _user(userId)
    if user != -1 and newLevel in _ALL_LEVELS:
        data[index]['level'] = newLevel
    else:
        core.log('ERROR', 'Invalid level change -> {} to level {}'.format(userId, newLevel))
        return -1
    _write_data()

def upgrade(userId):
    user, index = _user(userId)
    if user != -1:
        data[index]['level'] += 1
    else:
        core.log('ERROR', 'Invalid upgrading -> {}'.format(userId))
        return -1
    _write_data()

def degrade(userId):
    user, index = _user(userId)
    if user != -1:
        data[index]['level'] -= 1
    else:
        core.log('ERROR', 'Invalid degrading -> {}'.format(userId))
        return -1
    _write_data()

try:
    with open(_DATA_FILE) as dataFile:
        data = json.loads(dataFile.read())
except Exception as e:
    core.log('ERROR', 'Opening data file -> {}'.format(e))

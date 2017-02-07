def log(infoType, info):
    '''记录任何信息或错误。\ninfoType参数只支持INFO或ERROR。'''
    if infoType not in ('INFO', 'ERROR'):
        log('ERROR', 'Unknown Info Type -> {} ({})'.format(infoType, info))
        return -1
    print('[{}] {}'.format(infoType, info))

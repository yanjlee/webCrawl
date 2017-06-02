# coding=utf8

from Scence.config import USER_AGENT
import random

class header():
    def __init__(self, host=None):
        self.__host = host
    '''添加host构造headers'''
    def consHeaders(self, content):
        self.__host = content
        headers = {
            'Host': self.__host,
            'User-Agent': random.choice(USER_AGENT),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        return headers

    '''新添加项到headers'''
    def re_consHeaders(self, content, newKey, newValue):
        self.__host = content
        headers = {
            'Host': self.__host,
            'User-Agent': random.choice(USER_AGENT),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        headers[newKey] = newValue
        return headers
# coding=utf8
from config import USER_AGENT
import random

class headers:
    '''构造普通ua'''
    def make_headers(self, content):
        headers = {
            'Host': content,
            'User-Agent': random.choice(USER_AGENT),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

        return headers
    '''构造特殊ua'''
    def updata_headers(self, content, newKey, newValue):
        headers = {
            'Host': content,
            'User-Agent': random.choice(USER_AGENT),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        headers[newKey] = newValue
        return headers


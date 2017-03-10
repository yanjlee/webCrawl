# coding=utf8


import random
from . import USER_AGENT_LIST


class headers():
    def __init__(self, host):
        self.__host = host

    def consHeaders(self, content):
        self.__host = content
        headers = {
            'Host': self.__host,
            'User-Agent': random.choice(USER_AGENT_LIST),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        return headers

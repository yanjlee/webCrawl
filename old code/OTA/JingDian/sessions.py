# coding=utf8

import requests
from JingDian.headers import headers


class makeSession(headers):
    def __init__(self):
        self.__session = requests.session()
    def get_baidu_html(self, host, word):
        try:
            header = headers.consHeaders(self, host)
            url = 'https://lvyou.baidu.com/' + word
            return self.__session.get(url, headers=header, timeout=30).text
        except Exception as e:
            print(e)
            with open('data/errorBaidu.txt', 'a', encoding='utf-8') as f:
                f.writelines(url + '\n')
                







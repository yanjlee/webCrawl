# coding=utf8

import time
import requests
from Scence.headers import header

class setUpSession():
    def __init__(self):
        self.__header = header()
        self.__session = requests.session()
    def get_searchJson_from_qunar(self, prov, n):
        try:
            time.sleep(2)
            host = 'piao.qunar.com'
            headers = self.__header.consHeaders(host)
            url = 'http://piao.qunar.com/ticket/list.json'
            params = {
                'keyword': prov,
                'region': '',
                'from': 'mpl_search_suggest',
                'page': n
            }
            return self.__session.get(url, params=params, headers=headers, timeout=60).text
        except Exception as e:
            print(e)
            time.sleep(20)
            return False
    def get_sight_html_qunar(self, dict):
        try:
            time.sleep(2)
            host = 'piao.qunar.com'
            header = self.__header.consHeaders(host)
            url = 'http://piao.qunar.com/ticket/detail_' + str(dict["id"]) + '.html'
            return self.__session.get(url, timeout=60).text
        except Exception as e:
            print(e)
            time.sleep(20)
            return False

    def get_comment_from_qunar(self, ScenceId, n):
        try:
            time.sleep(2)
            host = 'piao.qunar.com'
            headers = self.__header.re_consHeaders(host,'X-Requested-With','XMLHttpRequest')
            url = 'http://piao.qunar.com/ticket/detailLight/sightCommentList.json'
            params = {
                'sightId': ScenceId,
                'index': n,
                'page': n,
                'pageSize': 1000,
                'tagType': 0
            }
            return self.__session.get(url, params=params, headers=headers, timeout=60).text
        except Exception as e:
            print(e)
            time.sleep(20)
            return False
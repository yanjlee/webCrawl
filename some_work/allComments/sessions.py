# coding=utf8

import requests, time
from headers import headers
class Elong_session:
    def __init__(self):
        self.headers = headers()
        self.session = requests.session()
    def get_info(self, hid, n):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/ajax/detail/gethotelreviews'
        headers = self.headers.updata_headers(host, 'X-Requested-With', 'XMLHttpRequest')
        time.sleep(3)
        params = {
            'hotelId': hid,
            'pageIndex': n,
            'code': '-99'
        }
        '''这里要返回,对page的大小做一个判断'''
        proxy = {
            'http': '112.91.135.115:8080',
            'http': '171.8.79.143:8080'
        }
        try:
            return self.session.get(url, headers=headers, params=params, proxies=proxy, timeout=30).text
        except:
            return False

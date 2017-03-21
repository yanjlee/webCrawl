# coding=utf8

import requests
import time
from HotelInfo.headers import headers

#作为请求的存在
class makeSession(headers):
    def __init__(self):
        self.__session = requests.session()
        self.__header = headers()


    def get_Json_data_fromElong(self, host, url):
        headers = self.__header.consHeaders(host)
        time.sleep(3)
        return self.__session.get(url, timeout=60).content.decode('utf-8')

    def get_xzq_fromElong(self, host, url):
        headers = self.__header.consHeaders(host)
        time.sleep(3)
        return self.__session.get(url, timeout=60).content.decode('utf-8')

    def get_hotelList_fromElong(self, host, url, cid, cn,aid, n):
        # try:
            headers = self.__header.consHeaders(host)
            data = {
                'listRequest.areaID': aid,
                'listRequest.cityID': cid,
                'listRequest.cityName': cn,
                'listRequest.pageIndex': n,
                'listRequest.pageSize': 20,
            }
            #使用代理
            # proxy = {
            #     'http': '106.46.136.61:808',
            #     'http': '60.209.90.211:8888'
            # }
            cookies = self.__session.get(url, headers=headers,timeout=60).cookies
            time.sleep(3)
            return self.__session.post(url, data=data, cookies=cookies, timeout=60).content.decode('utf-8')
        # except Exception as e:
        #     print(e)
        #     time.sleep(20)
        #     #添加没有抓成功的页面
        #     with open('Data/wrong_hotelList.txt', 'a', encoding='utf8') as f:
        #         f.writelines(str(aid) + '\u0001' + str(cid) + '\u0001' + str(cn) + '\u0001' + str(n) + '\u0001' + '\n')
        #     return False
    def get_info_from_hotel(self, host, url):
        headers = self.__header.consHeaders(host)
        time.sleep(10)
        return self.__session.get(url).content.decode('utf-8')

    def post_data_2_get_room_info(self, cne, hotelid, cid):
        referer = 'http://hotel.elong.com/' + cne + '/' + hotelid + '/'
        time.sleep(10)
        #必须要带referer和x-requested-with
        headers = {
            'Host': 'hotel.elong.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
            'Referer': referer,
            'X-Requested-With': 'XMLHttpRequest'
        }
        #post数据
        data = {
            'detailRequest.checkInDate': '2017-04-01',
            'detailRequest.checkOutDate': '2017-04-02',
            'detailRequest.cityId': cid,
            'detailRequest.citySeoNameEn': cne,
            'detailRequest.hotelIDs': hotelid
        }
        url = 'http://hotel.elong.com/ajax/detail/gethotelroomsetjva'
        return self.__session.post(url,headers=headers, data=data, timeout=60).content.decode('utf-8')

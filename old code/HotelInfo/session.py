# coding=utf8

import requests
import time, os
from HotelInfo.headers import headers
from HotelInfo.pipeline import Ctrip_pipe

#作为请求的存在
class makeSession(headers):
    def __init__(self):
        self.__session = requests.session()
        self.__header = headers()
        self.__pipeline = Ctrip_pipe()
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
            'code': '-99',
            'detailRequest.checkInDate': '2017-04-01',
            'detailRequest.checkOutDate': '2017-04-02',
            'detailRequest.cityId': cid,
            'detailRequest.citySeoNameEn': cne,
            'detailRequest.hotelIDs': hotelid
        }
        url = 'http://hotel.elong.com/ajax/detail/gethotelroomsetjva'
        return self.__session.post(url,headers=headers, data=data, timeout=60).content.decode('utf-8')

    '''----------------------------分割线-------------------------------------'''
    def get_home_page_from_Ctrip(self):
        host = 'hotels.ctrip.com'
        url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxGetCitySuggestion.aspx'
        headers = self.__header.consHeaders(host)
        response = self.__session.get(url, headers=headers)
        #更新cookies
        return response.text

    def get_city_html(self, dict):
        try:
            cnc = dict['cnc']
            cne = dict['cne']
            cid = dict['cid']
            host = 'hotels.ctrip.com'
            referer = 'http://hotels.ctrip.com/hotel/' + cne + cid
            headers = self.__header.re_consHeaders(host, 'Referer', referer)
            data = {
                'city': cid,
                'markType': '3'
            }
            proxies = {
                'http': '112.91.135.115:8080',
                'http': '61.186.164.97:8080'
            }
            url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxShowMoreDiv.aspx'
            time.sleep(3)
            city_html = self.__session.post(url,headers=headers, data=data, proxies=proxies, timeout=60).text
            html = '<div class="city" py="' + cne + '" id="' + cid + '">' + cnc + '</div>' + city_html
            return html
        except Exception as e:
            print(e)
            with open(os.path.join(os.path.abspath("Data"), "wrong_request_for_city.txt"), 'a', encoding='utf8') as f:
                f.writelines(cnc + '\u0001' + cne + '\u0001' + cid + '\n')
            return False

    def get_hotel_list(self, dict, n):
        try:
            cityId = dict['cityId']
            cityPY = dict['cityPY']
            cityloc = dict['location']
            url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
            host = 'hotels.ctrip.com'
            headers = self.__header.consHeaders(host)
            data = {
                'cityId': cityId,
                'cityPY': cityPY,
                'page': n,
                'location': cityloc,
                'checkIn': '2017-04-03',
                'checkOut': '2017-04-04'
            }
            proxies = {
                'http': '112.91.135.115:8080',
                'http': '61.186.164.97:8080'
            }
            time.sleep(5)
            r = requests.get(url, headers=headers, data=data, proxies=proxies, timeout=30)
            return r.text
        except Exception as e:
            print(e)
            return False

    def get_hoel_info(self, hid):
        host = 'hotels.ctrip.com'
        headers = self.__header.consHeaders(host)
        url = 'http://hotels.ctrip.com/hotel/' + hid + '.html'
        time.sleep(3)
        #这里缺一个return
        return self.__session.get(url, headers=headers).text

    def get_room_info(self, hid):
        host = 'hotels.ctrip.com'
        referer = 'http://hotels.ctrip.com/hotel/' + hid + '.html?isFull=F'
        headers = self.__header.re_consHeaders(host, 'Referer', referer)
        url = 'http://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx'
        params = {
            'hotel': hid,
            # 'city': '28',
            'startDate': '2017-04-01',
            'depDate': '2017-04-02',
        }
        return self.__session.get(url, params=params, headers=headers).text
# coding=utf8

'''
Info:
- author    : wangjiawei
- email     : wangjw@daqsoft.com.cn
- date      : 2017,03,20
Update:
- name      :
- email     :
- date      :
'''

from HotelInfo.session import makeSession
from HotelInfo.spyder.Elong_spyder import Elong_spyder
class Elong(object):
    '''
    作为艺龙的酒店数据引擎,先是获取城市列表,再根据列表开始抓数据.
    '''
    def __init__(self):
        self.CHECK = True
        self.response = makeSession()
        self.esp = Elong_spyder()
    '''从json中拿到城市列表'''
    def run_city(self):
        return self.get_cityList_from_json()

    def get_cityList_from_json(self):
        host = 'openapi.elong.com'
        for i in range(2,7):
            url = 'http://openapi.elong.com/suggest/hotcity/hotel/'+ str(i) +'.html'
            r = self.response.get_Json_data_fromElong(host, url)
            self.deal_json(r)

    def deal_json(self, r):
        self.esp.getDataFromJson(r)

    '''拿到各个城市的行政区'''
    def run_xzq(self):
        return self.get_xzqList_from_cities()

    def get_xzqList_from_cities(self):
        #先获得城市列表
        t = open('Data/Elong_citiesList.txt', 'r', encoding='utf8').readlines()
        for i in range(len(t)):
            print(i)
            list = t[i].split('\u0001')
            id = list[0]
            nc = list[1]
            ne = list[2].replace('\n', '')
            self.getHtml(id, nc, ne)

    def getHtml(self, id, nc, ne):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/' + ne + '/'
        r = self.response.get_xzq_fromElong(host, url)
        self.deal_html(r, id, nc, ne)
    def deal_html(self,content, id, nc, ne):
        self.esp.getHtmlFromContent(content, id, nc, ne)
    '''从各个城市行政区出发,拿到酒店列表'''
    def run_hotelList(self):
        return self.get_hotelList_from_xzq()

    def get_hotelList_from_xzq(self):
        #先拿到行政区列表
        t = open('Data/Elong_xzqList.txt', 'r', encoding='utf-8').readlines()
        for i in range(len(t)):
            print(i)
            list = t[i].split('\u0001')
            cityid = list[0]
            citync = list[1]
            cityne = list[2]
            xzqnc = list[3]
            xzqid = list[4]
            self.get_HotelList_from_json(cityid, citync, xzqnc, xzqid, cityne)

    def get_HotelList_from_json(self, cityid, citync, xzqnc, xzqid, cityne):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/ajax/list/asyncsearch'
        n = 1
        while self.CHECK:
            r = self.response.get_hotelList_fromElong(host, url, cityid, citync, xzqid, n)
            if r:
                self.CHECK = self.do_judge_for_circle(r)
                if self.CHECK:
                    self.deal_HotelList_from_json(r, cityid, citync, xzqnc, xzqid, cityne)
                    n += 1
            else:
                self.CHECK = False
        self.CHECK = True

    def do_judge_for_circle(self, content):
        '''这里要返回一个结果,让循环继续还是停止'''
        return self.esp.do_judge(content)

    def deal_HotelList_from_json(self, content,cityid, citync, xzqnc, xzqid, cityne):
        self.esp.deal_json_for_hotelList(content, cityid, citync, xzqnc, xzqid, cityne)

    '''开始拿酒店信息'''
    def run_hotelInfo(self):
        return self.set_up_circle()
    def set_up_circle(self):
        t = open('Data/Elong_hotelList.txt', 'r', encoding='utf-8').readlines()
        for i in range(len(t)):
        # for i in range(7,9):
            list = t[i].split('\u0001')
            cid = list[0]
            cnc = list[1]
            cne = list[2]
            aid = list[3]
            anc = list[4]
            hid = list[5]
            self.get_hotel_base_data(cnc, cne, aid, anc, hid)
            # self.get_hotel_room_data(cne, hid, cid, anc, cnc)

    def get_hotel_base_data(self, cnc, cne, aid, anc, hid):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/' + cne + '/' + hid + '/'
        r = self.response.get_info_from_hotel(host, url)
        self.deal_hotel_base_data(r, cnc, anc, hid)

    def deal_hotel_base_data(self, content, cnc, anc, hid):
        self.esp.get_hotel_base_data(content, cnc, anc, hid)

    def get_hotel_room_data(self, cne, hid, cid, anc, cnc):
        r = self.response.post_data_2_get_room_info(cne, hid, cid)
        self.deal_hotel_room_data(r, cnc, anc, hid)
    def deal_hotel_room_data(self, r, cnc, anc, hid):
        self.esp.get_hotel_room_data(r, cnc, anc, hid)

if __name__ == '__main__':
    e = Elong()
    # e.run_hotelList()
    # e.run_xzq()
    e.run_hotelInfo()
# coding=utf8

import json
import re
from lxml import etree
from HotelInfo.pipeline import Ctrip_pipe
import requests
class ctrip_spyder():
    def __init__(self):
        self.pipeline = Ctrip_pipe()
    def get_data_of_cities(self, content):
        selector = etree.HTML(content)
        cons = selector.xpath('//div[@class="city_item"]/div[@class="city_item_in"]')
        data = []
        for each in cons:
            num = len(each.xpath('a/text()'))
            for i in range(num):
                city = {}
                city['cnc'] = each.xpath('a/text()')[i]
                city['cne'] = each.xpath('a/@title')[i]
                city['cid'] = each.xpath('a/@data-id')[i]
                data.append(city)

        return self.pipeline.get_list_data(data)

    def get_xzq_data(self, content):
        selector = etree.HTML(content)
        cnc = selector.xpath('//div[@class="city"]/text()')[0]
        cne = selector.xpath('//div[@class="city"]/@py')[0]
        cid = selector.xpath('//div[@class="city"]/@id')[0]
        for each in selector.xpath('//div[@class="area_list"]/a'):
            xz = {}
            fs = {}
            url = each.xpath('@href')[0]
            if url == 'javascript:;':
                #行政区
                xz['cnc'] = cnc
                xz['cne'] = cne
                xz['cid'] = cid
                xz['anc'] = each.xpath('text()')[0]
                xz['aid'] = each.xpath('@data-value')[0]
                self.pipeline.transporting_xz(xz)
            else:
                #附属县市
                fs['cnc'] = cnc
                fs['cne'] = cne
                fs['cid'] = cid
                fs['a_url'] = url
                fs['fnc'] = each.xpath('@title')[0]
                self.pipeline.transporting_fs(fs)
    '''------------酒店列表-----------------'''
    #先是各县成的酒店
    def get_data_from_json(self, info, content):
        dict = {} #作为数据返回用的字典
        jsDict = json.loads(content)
        dict['hotel_list'] = jsDict["hotelIds"]
        self.pipeline.deal_hotelList_data(info, dict)

    '''--------------收集酒店数据-----------------'''
    def get_hotel_data(self, content, hid):
        hotel = {}
        selector = etree.HTML(content)
        hotel['hid'] = hid
        hotel['con'] = selector.xpath('//div[@class="main_detail_wrapper "]/div/div[@class="htl_info"]/div[2]/h2/text()')
        if selector.xpath('//div[@class="main_detail_wrapper "]/div/div[@class="htl_info"]/div[3]/span/@title'):
            hotel['star'] = selector.xpath('//div[@class="main_detail_wrapper "]/div/div[@class="htl_info"]/div[3]/span/@title')[0]
        else:
            hotel['star'] = ''
        if selector.xpath('//div[@class="main_detail_wrapper "]/div/div[@class="htl_info"]/div[4]'):
            hotel['address'] = selector.xpath('//div[@class="main_detail_wrapper "]/div/div[@class="htl_info"]/div[4]')[0].xpath('string(.)')
        else:
            hotel['address'] = ''
        # hotel_rooms = selector.xpath('//div[@id="hotel_info_comment"]/div/div[@class="htl_room_txt text_3l "]/p/text()')
        if selector.xpath('//div[@id="hotel_info_comment"]/div/div[@class="htl_room_txt text_3l "]/p'):
            hotel['hotel_info'] = selector.xpath('//div[@id="hotel_info_comment"]/div/div[@class="htl_room_txt text_3l "]/p')[0].xpath('string(.)')
        else:
            hotel['hotel_info'] = ''
        # 酒店设施
        hotel_sheshi = selector.xpath('//div[@id="hotel_info_comment"]/div/div[@id="J_htl_facilities"]/table/tbody/tr')
        for each in hotel_sheshi:
            if each.xpath('th'):
                hotel[each.xpath('th/text()')[0]] = each.xpath('td/ul')[0].xpath('string(.)')
        #酒店政策
        hotel_zc = selector.xpath('//table[@class="detail_extracontent"]/tr')
        for each in hotel_zc:
            if each.xpath('th'):
                if each.xpath('td/div/span'):
                    hotel[each.xpath('th/text()')[0]] = self.get_card_info(each.xpath('td/div/span'))
                else:
                    hotel[each.xpath('th/text()')[0]] = each.xpath('td')[0].xpath('string(.)')
        #酒店数据采集结束,交给pipeline
        return self.pipeline.deal_hotel_info(hotel)
    def get_card_info(self, cons):
        crds = ''
        for each in cons:
            t = re.findall('<div class="jmp_bd">(.*?)\'}', each.xpath('@data-params')[0], re.S)[0].replace('</div>', '')
            crds += t
        return crds

    '''------------------------------------------'''

    def get_room_data(self, content, hid):
        info = {}
        info['hid'] = hid
        jsDict = json.loads(content)["html"]
        selector = etree.HTML(jsDict)
        #额外信息
        rinfo = selector.xpath('//div[@class="htl_room_table J_roomTable"]/table/tr[@class="clicked hidden"]')
        text = []
        for each2 in rinfo:
            text.append(each2.xpath('td/div/div[@class="searchresult_caplist_box"]/ul/li/text()'))
        #基本信息
        con = selector.xpath('//div[@class="htl_room_table J_roomTable"]/table/tr[@class=""]')
        num = len(con)
        n = 0
        for each in con:
            info['name'] = each.xpath('td[1]/a[2]/text()')
            info['bed'] = each.xpath('td[3]/text()')
            info['bf'] = each.xpath('td[4]/text()')
            info['wifi'] = each.xpath('td[5]/span/text()')
            info['num'] = each.xpath('td[6]/span/@title')
            info['price'] = each.xpath('td[8]/p[1]/span/text()')
            for i in text[n]:
                if '建筑面积' in i:
                    info['area'] = i
                if '楼层' in i:
                    info['floor'] = i
                if '可加床' in i:
                   info['addBed'] = i
            n += 1
        #数据提交到pipeline
        print(info)
        # return self.pipeline.deal_room_info(info)



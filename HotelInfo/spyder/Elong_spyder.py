# coding=utf8

import json
import re
from lxml import etree

class Elong_spyder():
    #这里处理艺龙的json数据,需要cityid,citynamecn,citynameen,
    def getDataFromJson(self, content):
        return self.dealDataForElong(content)

    def dealDataForElong(self, content):
        jsDict = json.loads(content)["result"]["cityList"]
        for each in jsDict:
            text = ''
            self.__cityid = each["cityId"]
            if re.findall('(.*)（', each["cityNameCn"], re.S):
                self.__citync = re.findall('(.*)（', each["cityNameCn"], re.S)[0]
            else:
                self.__citync = each["cityNameCn"]
            if re.findall('（(.*?)）', each["cityNameEn"], re.S):
                self.__cityne = re.findall('（(.*?)）', each["cityNameEn"], re.S)[0]
            else:
                self.__cityne = each["cityNameEn"]
            text = self.__cityid + self.__column_split + self.__citync + self.__column_split + self.__cityne + '\n'
            self.save_json(text)

    #保存json
    def save_json(self, text):
        with open('Data/Elong_citiesList.txt', 'a', encoding='utf-8') as f:
            f.writelines(text)
    '''-------------------分割线-----------------------------------'''
    def getHtmlFromContent(self, content, id, nc, ne):
        return self.dealDataFromContent(content, id, nc, ne)

    def dealDataFromContent(self, content, id, nc, ne):
        selector = etree.HTML(content)
        area = selector.xpath('//li[@data-typeid="4"]')
        if area:
            for each in area:
                if each.xpath('@data-id'):
                    text = ''
                    self.__areaId = each.xpath('@data-id')[0]
                    self.__areaName = each.xpath('@title')[0]
                    text = '%s%s%s%s%s%s%s%s%s%s' %(id, self.__column_split, nc, self.__column_split, ne,
                                                    self.__column_split, self.__areaName, self.__column_split,
                                                    self.__areaId, self.__column_split)
                    self.save_xzq(text)

    def save_xzq(self, text):
        print(text)
        with open('Data/Elong_xzqList.txt', 'a', encoding='utf-8') as f:
            f.writelines(text + '\n')
    '''----------------分割线-------------------------------'''
    #处理酒店列表的json
    def do_judge(self, content):
        if re.findall('"hotelCount":(\d{1,4}),"pageDownHtml"', content, re.S):
            jsCount = json.loads(content)["value"]["hotelCount"]
            if jsCount == 0:
                return False
            else:
                return True
        else:
            return False

    def deal_json_for_hotelList(self, content, cid, cn, xn, xid, cne):
        jsDict = json.loads(content)["value"]["hotelIds"]
        list = jsDict.split(',')
        for each in list:
            text = '%s%s%s%s%s%s%s%s%s%s%s%s' \
                   %(str(cid), self.__column_split, str(cn), self.__column_split, str(cne), self.__column_split, str(xid),
                     self.__column_split, str(xn), self.__column_split, str(each), self.__column_split)
            self.save_hotelList(text)

    def save_hotelList(self, text):
        with open('Data/Elong_hotelList.txt', 'a', encoding='utf-8') as f:
            f.writelines(text + '\n')
    '''---------------分割线------------------------------'''
    def get_hotel_base_data(self, content, cnc, anc, hid):
        selector = etree.HTML(content)
        self.__h_name = selector.xpath('//div[@class="hdetail_rela_wrap"]/div/div/div/div/@title')[0]
        self.__h_address = selector.xpath('//div[@class="hdetail_rela_wrap"]/div/div/div/p/span/text()')[1]
        self.__h_type = selector.xpath('//div[@class="hdetail_rela_wrap"]/div/div/div/div/b/@title')
        if self.__h_type:
            self.__h_type = re.findall('艺龙用户评定为(.*)', self.__h_type[0], re.S)[0]
        else:
            self.__h_type = ''
        if selector.xpath('//div[@class="hrela_faci"]/div/i'):
            for each in selector.xpath('//div[@class="hrela_faci"]/div/i'):
                self.__h_fuwu += each.xpath('@title')[0] + ','
        #酒店信息
        con = selector.xpath('//div[@id="hotelContent"]/div/dl')
        self.__h_info = {}
        for each in con:
            if each.xpath('dt/text()'):
                name = each.xpath('dt/text()')[0]
                if each.xpath('dd/p/text()'):
                    ctd = each.xpath('dd/p/text()')
                elif each.xpath('dd/text()'):
                    ctd = each.xpath('dd/text()')
                values = ctd[0].replace('\t', '').replace('\n', '').replace(' ', '')
                self.__h_info[name] = values
        #获取信用卡
        cards = selector.xpath('//div[@id="hotelContent"]/div/dl[@class="dview_info_item dview_info_card"]/dd/i')
        cds = ''
        for card in cards:
            cds += self.credit_card(card.xpath('@class')[0]) + ','
        self.__h_info['可接受的信用卡'] = cds
        #提取内容
        if '可接受的信用卡' in self.__h_info.keys():
            crds = self.__h_info['可接受的信用卡']
        else:
            crds = ''
        if '酒店设施' in self.__h_info.keys():
            sheshi = self.__h_info['酒店设施']
        else:
            sheshi = ''
        if '停车场' in self.__h_info.keys():
            prks = self.__h_info['停车场']
        else:
            prks = ''
        if '开业时间' in self.__h_info.keys():
            otime = self.__h_info['开业时间']
        else:
            otime = ''
        if '酒店简介' in self.__h_info.keys():
            jj = self.__h_info['酒店简介']
        else:
            jj = ''
        if '酒店服务' in self.__h_info.keys():
            self.__h_fuwu += self.__h_info['酒店服务']
        if '入离时间' in self.__h_info.keys():
            time = self.__h_info['入离时间']
        if '酒店电话' in self.__h_info.keys():
            tel = self.__h_info['酒店电话']
        else:
            tel = ''
        #写入数据 酒店名字+地址+类型+电话+时间+停车+开业+设施+服务+简介+信用卡
        text = cnc + self.__column_split + anc + self.__column_split+ hid + self.__h_name + self.__column_split + self.__h_address + self.__column_split +\
               self.__h_type + self.__column_split + tel + self.__column_split + time + self.__column_split + prks + \
               self.__column_split + otime + self.__column_split + sheshi + self.__column_split + self.__h_fuwu +\
               self.__column_split + jj + self.__column_split + crds + self.__column_split + '\n'
        self.save_hb(text)
        print(text)
    # 以下为房间信息
    def get_hotel_room_data(self, content, cnc, anc, hid):
        jcon = json.loads(content)["value"]["content"]
        selector = etree.HTML(jcon)
        con = selector.xpath('//div[@class="htype_item on"]')

        for each in con:
            f = ''
            # 类型
            rtype = each.xpath('div[2]/div[3]/p[1]/span/text()')
            f += rtype[0] + '\u0001'
            # 数据
            con = each.xpath('div[2]/div[3]/p[2]/span')
            for n in con:
                if n.xpath('i'):
                    t = n.xpath('text()')[0].replace('\n', '')
                    tt = len(n.xpath('i'))
                    f += t + str(tt) + '人'
                else:
                    f += n.xpath('text()')[0].replace('\n', '').replace('|', '\u0001')
            # 价格
            f += '\u0001' + each.xpath('div[2]/div[2]/p[1]')[0].xpath('string(.)').replace('\n', '').replace(' ', '')
            # 额外信息
            f += '\u0001' + each.xpath('div[3]/table/tbody/tr[@class="ht_tr_other"]/td[2]')[0].xpath('string(.)'). \
                replace('\n', '').replace('\t', '').replace('\r', '。')
            #获取加床费
            if each.xpath('div[1]/p/@data-sroomid'):
                fee = self.judge_fee(content, each.xpath('div[1]/p/@data-sroomid')[0])
                if fee:
                    fee = fee
                else:
                    fee = '不提供加床服务。'
            else:
                fee = '不提供加床服务。'
            f += '\u0001' + fee
            text = cnc + '\u0001' + anc + '\u0001' + hid + '\u0001' + f + '\u0001' + '\n'
            self.save_hr(text)

    def judge_fee(self, content, numb):
        jsDict = json.loads(content)["value"]["hotelTipInfo"]["productsInfo"]
        for each in jsDict:
            if each["sRoomID"] == numb:
                return each["productAttachDesc"][0]["value"]



    def credit_card(self, cds):
        if cds == 'icon_card2':
            return 'Visa'
        elif cds == 'icon_card6':
            return '银联'
        elif cds == 'icon_card3':
            return 'Master card'
        elif cds == 'icon_card1':
            return 'american express'
        elif cds == 'icon_card5':
            return '大莱信用卡'
        elif cds == 'icon_card4':
            return 'JBC'
        else:
            return None

    def save_hb(self, text):
        with open('Data/data_hotel_base.txt', 'a', encoding='utf-8') as f:
            f.writelines(text)
    def save_hr(self, text):
        with open('Data/data_hotel_room.txt', 'a', encoding='utf-8') as f:
            f.writelines(text)

    def __init__(self, cityid='', citynamecn='', citynameen='', column_split='\u0001', areaId='', areaName='',
                 h_name='', h_address='', h_type='', h_fuwu='', h_info=''):
        self.__cityid = cityid
        self.__citync = citynamecn
        self.__cityne = citynameen
        self.__column_split = column_split
        self.__areaId = areaId
        self.__areaName = areaName
        self.__h_name = h_name
        self.__h_address = h_address
        self.__h_type = h_type
        self.__h_fuwu = h_fuwu
        self.__h_info = h_info
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
            cityid = each["cityId"]
            if re.findall('(.*)（', each["cityNameCn"], re.S):
                citync = re.findall('(.*)（', each["cityNameCn"], re.S)[0]
            else:
                citync = each["cityNameCn"]
            if re.findall('（(.*?)）', each["cityNameEn"], re.S):
                cityne = re.findall('（(.*?)）', each["cityNameEn"], re.S)[0]
            else:
                cityne = each["cityNameEn"]
            text = cityid + '\u0001' + citync + '\u0001' + cityne + '\n'
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
                    areaId = each.xpath('@data-id')[0]
                    areaName = each.xpath('@title')[0]
                    text = '%s%s%s%s%s%s%s%s%s%s' %(id, '\u0001', nc, '\u0001', ne,
                                                    '\u0001', areaName, '\u0001',
                                                    areaId, '\u0001')
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
                   %(str(cid), '\u0001', str(cn), '\u0001', str(cne), '\u0001', str(xid),
                     '\u0001', str(xn), '\u0001', str(each), '\u0001')
            self.save_hotelList(text)

    def save_hotelList(self, text):
        with open('Data/Elong_hotelList.txt', 'a', encoding='utf-8') as f:
            f.writelines(text + '\n')
    '''---------------分割线------------------------------'''
    def get_hotel_base_data(self, content, cnc, anc, hid):
        try:
            selector = etree.HTML(content)
            hname = selector.xpath('//div[@class="hdetail_rela_wrap"]/div/div/div/div/@title')[0]
            address = selector.xpath('//div[@class="hdetail_rela_wrap"]/div/div/div/p/span/text()')[1]
            type = selector.xpath('//div[@class="hdetail_rela_wrap"]/div/div/div/div/b/@title')
            if type:
                if re.findall('艺龙用户评定为(.*)', type[0], re.S):
                    type = re.findall('艺龙用户评定为(.*)', type[0], re.S)[0]
                else:
                    type = type[0]
            else:
                type = ''
            if selector.xpath('//div[@class="hrela_faci"]/div/i'):
                fuwu = ''
                for each in selector.xpath('//div[@class="hrela_faci"]/div/i'):
                    fuwu += each.xpath('@title')[0] + ','
            #酒店信息
            con = selector.xpath('//div[@id="hotelContent"]/div/dl')
            info = {}
            for each in con:
                if each.xpath('dt/text()'):
                    name = each.xpath('dt/text()')[0]
                    if each.xpath('dd/p/text()'):
                        ctd = each.xpath('dd/p/text()')
                    elif each.xpath('dd/text()'):
                        ctd = each.xpath('dd/text()')
                    values = ctd[0].replace('\t', '').replace('\n', '').replace(' ', '')
                    info[name] = values
            #获取信用卡
            cards = selector.xpath('//div[@id="hotelContent"]/div/dl[@class="dview_info_item dview_info_card"]/dd/i')
            cds = ''
            for card in cards:
                cds += self.credit_card(card.xpath('@class')[0]) + ','
            info['可接受的信用卡'] = cds
            #提取内容
            if '可接受的信用卡' in info.keys():
                crds = info['可接受的信用卡']
            else:
                crds = ''
            if '酒店设施' in info.keys():
                sheshi = info['酒店设施']
            else:
                sheshi = ''
            if '停车场' in info.keys():
                prks = info['停车场']
            else:
                prks = ''
            if '开业时间' in info.keys():
                otime = info['开业时间']
            else:
                otime = ''
            if '酒店简介' in info.keys():
                jj = info['酒店简介']
            else:
                jj = ''
            if '酒店服务' in info.keys():
                fuwu += info['酒店服务']
            if '入离时间' in info.keys():
                time = info['入离时间']
            else:
                time = ''
            if '酒店电话' in info.keys():
                tel = info['酒店电话']
            else:
                tel = ''
            #写入数据 酒店名字+地址+类型+电话+时间+停车+开业+设施+服务+简介+信用卡
            text = cnc + '\u0001' + anc + '\u0001' + hid + '\u0001' + hname + \
                   '\u0001' +address + '\u0001' +type + \
                   '\u0001' + tel + '\u0001' +time + '\u0001' + prks + \
                   '\u0001' + otime + '\u0001' + sheshi + '\u0001' + fuwu + \
                   '\u0001' + jj + '\u0001' + crds + '\u0001' + '\n'
            self.save_hb(text)
        except Exception as e:
            print(e)

    # 以下为房间信息
    def get_hotel_room_data(self, content, cnc, anc, hid):
        # if re.findall('"content":"(.*?)","hasHighSpeed"', content, re.S):
        try:
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
        except Exception as e:
            print(e)
            with open('Data/wrong_hotel_room.txt', 'a', encoding='utf8') as f:
                f.writelines(cnc + '\u0001' + hid + '\u0001' + '\n')

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

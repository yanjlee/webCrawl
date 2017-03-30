# coding=utf8
import os
import re
import json

class Ctrip_pipe():
    def get_list_data(self, list):
        return self.deal_data_for_cities(list)

    def deal_data_for_cities(self, list):
        for each in list:
            text = each['cnc'] + '\u0001' + each['cne'] + '\u0001' + each['cid'] + '\u0001'
            self.save_data_as_cities(text)
    #
    # def save_data_as_cities(self, text):
    #     with open(os.path.join(os.path.abspath("Data"), "Ctrip_cities_code.txt"), 'a', encoding='utf-8') as f:
    #         f.writelines(text + '\n')
    '''---------------各城市行政区------------------'''
    def get_city_info(self):
        for each in open(os.path.join(os.path.abspath("Data"), "Ctrip_cities_code.txt"), 'r', encoding='utf-8'):
            yield each

    def deal_each_city(self):
        return open(os.path.join(os.path.abspath("Data"),"Ctrip_cities_code.txt"), 'r', encoding='utf8')
    def deal_each_city_into_dict(self, city):

        c = {}
        c['cnc'] = city.split('\u0001')[0]
        c['cne'] = city.split('\u0001')[1]
        c['cid'] = city.split('\u0001')[2]
        return c
    #保存行政区
    def save_page_for_ctrip_city(self, cont, cnc, cne, cid):
        text = '<div class="city" py="' + cne + '" id="' + cid +'">' + cnc + '</div>' + cont
        # with open(os.path.join(os.path.abspath("html"), "Ctrip_city_xzq.txt"), 'w', encoding='utf-8') as f:
        #     f.write(text)
        return text

    #线程spyder从中转站里拿文件
    def get_html_from_html(self):
        return open(os.path.join(os.path.abspath("html"),"Ctrip_city_xzq.txt"), 'r', encoding='utf-8').read()

    def transporting_xz(self, dict):
        text = '%s%s%s%s%s%s%s%s%s%s' %(dict['cnc'], '\u0001', dict['cne'], '\u0001', dict['cid'], '\u0001',
                                        dict['anc'], '\u0001', dict['aid'], '\u0001')
        with open(os.path.join(os.path.abspath("Data"), "Ctrip_city_zxq.txt"),'a', encoding='utf-8') as f:
            f.writelines(text + '\n')

    def transporting_fs(self, dict):
        text = '%s%s%s%s%s%s%s%s%s%s' %(dict['cnc'], '\u0001', dict['cne'], '\u0001', dict['cid'], '\u0001',
                                        dict['a_url'], '\u0001', dict['fnc'], '\u0001')
        with open(os.path.join(os.path.abspath("Data"), "Ctrip_city_fs.txt"),'a', encoding='utf-8') as f:
            f.writelines(text + '\n')
    '''------------------分割线----------------------'''
    def deal_each_area_code(self, content):
        cons = content.split('\u0001')
        dict = {}
        if 'hotel' in cons[3]:
            #说明是县城
            dict['cnc'] = cons[0]
            dict['cityId'] = re.findall('\d{2,5}', cons[3], re.S)[0]
            dict['cityPY'] = re.findall('(.*?)\d', cons[3].split('/')[2])[0]
            dict['anc'] = cons[4]
            dict['location'] = ''

        else:
            dict['anc'] = cons[3]
            dict['cnc'] = cons[0]
            dict['cityId'] = cons[2]
            dict['cityPY'] = cons[1]
            dict['location'] = cons[4]
        return dict

    def do_judge(self, content):
        try:
            dict = {}  # 作为数据返回用的字典
            jsDict = json.loads(content)
            if jsDict["hotelIds"] != '':
                return True
            else:
                return False
        except Exception as e:
            print(e)
    def deal_hotelList_data(self, info, dict):
        try:
            cnc = info['cnc']
            anc = info['anc']
            hotlist = dict['hotel_list'].split(',')
            for each in hotlist:
                text = cnc + '\u0001' + anc + '\u0001' + each.split('_')[0] + '\u0001'
                self.save_as_hotelList(text)
        except Exception as e:
            print(e)
    def save_as_hotelList(self, text):
        with open(os.path.join(os.path.abspath("Data"), "Ctrip_hotel_list.txt"), 'a', encoding='utf-8') as f:
            f.writelines(text + '\n')
    '''-----------酒店信息-------------'''
    def deal_each_hotel(self, content):
        return content.split('\u0001')[2]

    def deal_hotel_info(self, hotel):
        hid = hotel['hid']
        hnc = hotel['con'][0]
        hloc = hotel['address'].replace('\n', '').replace(' ', '')
        hgrade = hotel['star']
        hinfo = hotel['hotel_info'].replace('\n', '').replace('\xa0', '').replace('\u3000', '').replace(' ', '')
        if '通用设施' in hotel.keys():
            htyss = hotel['通用设施']
        else:
            htyss = ''
        if '活动设施' in hotel.keys():
            hhdss = hotel['活动设施']
        else:
            hhdss = ''
        if '服务项目' in hotel.keys():
            hfwxm = hotel['服务项目']
        else:
            hfwxm = ''
        if '客房设施' in hotel.keys():
            hkfss = hotel['客房设施']
        else:
            hkfss = ''
        if '入住和离店' in hotel.keys():
            hrzld = hotel['入住和离店'].replace('\n', '')
        else:
            hrzld = ''
        if '儿童政策' in hotel.keys():
            hkids = hotel['儿童政策'].replace('\n', '')
        else:
            hkids = ''
        if '膳食安排' in hotel.keys():
            hssap = hotel['膳食安排'].replace('\n', '')
        else:
            hssap = ''
        if '宠物' in hotel.keys():
            hpets = hotel['宠物'].replace('\n', '')
        else:
            hpets = ''
        if '接受信用卡' in hotel.keys():
            hcards = hotel['接受信用卡'].replace('\n', '')
        else:
            hcards = ''
        text = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' \
               %(hid, '\u0001', hnc,'\u0001', hloc,'\u0001', hgrade,'\u0001', hinfo,'\u0001', htyss,'\u0001', hhdss,
                 '\u0001', hfwxm,'\u0001', hkfss,'\u0001', hrzld,'\u0001', hkids,'\u0001', hssap,'\u0001',
                 hpets,'\u0001', hcards,'\u0001')
        self.sava_as_hotel_info(text)
    def sava_as_hotel_info(self, text):
        with open(os.path.join(os.path.abspath("Data"), "Ctrip_hotel_Base.txt"), 'a', encoding='utf-8') as f:
            f.writelines(text + '\n')

    def deal_room_info(self, room):
        hid = room['hid']
        name = room['name'][0].replace('\n', '')
        bed = room['bed'][0].replace('\n', '')
        num = room['num'][0].replace('\n','')
        wifi = room['wifi'][0].replace('\n', '')
        bf = room['bf'][0].replace('\n', '')
        price = room['price'][0].replace('\n', '')
        area = room['area'].replace('\n', '')
        floor = room['floor'].replace('\n', '')
        text = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s'\
               %(hid, '\u0001', name, '\u0001', bed, '\u0001', num, '\u0001', wifi,
                 '\u0001', bf, '\u0001', price, '\u0001', area, '\u0001', floor, '\u0001')
        self.save_as_room_info(text)
    def save_as_room_info(self, text):
        with open(os.path.join(os.path.abspath("Data"), "Ctrip_room_info.txt"), 'a', encoding='utf-8') as f:
            f.writelines(text + '\n')
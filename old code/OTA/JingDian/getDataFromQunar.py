# coding=utf8

'''
Info:
- author    : wangjiawei
- email     : wangjw@daqsoft.com.cn
- date      : 2017,03,07
Update:
- name      :
- email     :
- date      :
'''


import requests
import json
import random
import time
import re
import os
from urllib import request
from lxml import etree
from JingDian import USER_AGENT_LIST

#配置
class setting():
    ua = random.choice(USER_AGENT_LIST)
    host = 'piao.qunar.com'
    headers = {
        'User-Agent': ua,
        'Host': host,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
#从list.txt列表里提取数据,放入list里
class loadInList():
    list_a = open('list.txt', 'r').readlines()
    #去'\n'
    list_b = []
    for i in list_a:
        list_b.append(i.replace('\n', ''))


#建立session,不需要登录就没有登录模块
class setUpSession(setting):
    session = requests.session()
    session.headers.update(setting.headers)
    def get_json(params):
        url = 'http://search.piao.qunar.com/sight/suggestWithId.jsonp'
        params = {
            'key': params
        }
        return setUpSession.session.get(url, params=params).text
    def get_url(keyword):
        url = 'http://piao.qunar.com/ticket/list.htm'
        params = {
            'keyword': keyword
        }
        return setUpSession.session.get(url, params=params).text
    def get_page(num):
        url = 'http://piao.qunar.com/ticket/detail_' + num + '.html'
        return setUpSession.session.get(url).text

#录入json中的数据
class dealWithJson(setUpSession):
    def __init__(self, column_split='\u0001'):
        self.column_split = column_split
    #建立session
    def makeSession(self):
        json_list = loadInList.list_b
        for each in json_list:
            #既然是继承,这里就要重写
            response = setUpSession.get_json(each)
            self.dealJson(response)
            time.sleep(3)
            break
    #处理json数据
    def dealJson(self, content):
        jsDict = json.loads(content)['s']
        for each in jsDict:
            l = each.split(',')
            text = ''
            for i in l:
                text += i + self.column_split
            print('录入:' + text)
            with open('search_list.txt', 'a') as f:
                f.writelines(text + '\n')

#关于页面数据的提取
class getJingDianData(setUpSession):
    def __init__(self, column_spilt='\u0001', name=None, loc=None, num=None, type=None, jd_star=None, jd_name=None,
                 jd_miaosu=None, jd_loc=None, baidu_point=None, google_point=None, jd_Tel=None, jd_jianjie=None,
                 jd_shijian=None, jd_tese=None, jd_teseContent=None, jd_price=None, jd_ruyuan=None, jd_tips=None,
                 jd_traffic=None):
        self.column_split = column_spilt
        self.name = name,
        self.loc = loc,
        self.num = num,
        self.type = type
        self.jd_star = jd_star,
        self.jd_name = jd_name,
        self.jd_miaosu = jd_miaosu
        self.jd_loc = jd_loc
        self.baidu_point = baidu_point,
        self.google_point = google_point,
        self.jd_Tel = jd_Tel
        self.jd_jianjie = jd_jianjie
        self.jd_shijian = jd_shijian
        self.jd_tese = jd_tese
        self.jd_teseContent = jd_teseContent
        self.jd_price = jd_price
        self.jd_ruyuan = jd_ruyuan
        self.jd_tips = jd_tips
        self.jd_traffic = jd_traffic
        self.item = []
    #获取搜索列表
    def get_List(self):
        list = loadInList.list_b
        self.makeSession_url(list)
    def makeSession_url(self, content):
        for each in content:
            response = setUpSession.get_url(each)
            selector = etree.HTML(response)
            if selector.xpath('//a[@class="sight_item_do"][1]/@href'):
                url = selector.xpath('//a[@class="sight_item_do"][1]/@href')[0]
                self.num = re.findall('/ticket/detail_(.*?).html', url, re.S)[0]
                self.makeSession(self.num, each)
                time.sleep(1)
            else:
                continue
        print('抓取完毕,失效的有')
        for i in self.item:
            with open('exdata.txt', 'a') as f:
                f.writelines(i + '\n')
    def getNum(self):
        data_list = open('search_list.txt', 'r', encoding='utf8').readlines()
        text = []
        for each in data_list:
            self.num = each.split('\u0001')[2]
            self.makeSession(self.num, each)
            time.sleep(3)

    def makeSession(self,num, item):
        response = setUpSession.get_page(num)

        return self.spyder(response, item)
    #获取景点经纬度和电话
    def get_jingweiduAndTel(self, response):
        text = re.findall('window.context =(.*?)window.context', response, re.S)[0]
        if re.findall('"baiduPoint": "(.*?)",', text, re.S):
            self.baidu_point = re.findall('"baiduPoint": "(.*?)",', text, re.S)[0]
        if re.findall('"googlePoint": "(.*?)",', text, re.S):
            self.google_point = re.findall('"googlePoint": "(.*?)",', text, re.S)[0]
        if re.findall('"phone": "(.*?)",', text, re.S):
            self.jd_Tel = re.findall('"phone": "(.*?)",', text, re.S)[0]

    def spyder(self, response, item):
        selector = etree.HTML(response)
        #景区名字
        try:
            self.jd_name = selector.xpath('//div[@class="mp-description-view"]/span[1]/text()')[0]
            #景区等级
            if selector.xpath('//div[@class="mp-description-view"]/span[2]'):
                self.jd_star = selector.xpath('//div[@class="mp-description-view"]/span[2]/text()')[0]

            #景区一句话描述
            if selector.xpath('//div[@class="mp-description-onesentence"]/text()'):
                self.jd_miaosu = selector.xpath('//div[@class="mp-description-onesentence"]/text()')[0]

            #景区位置
            if selector.xpath('//div[@class="mp-description-location"]/span[3]/text()'):
                self.jd_loc = selector.xpath('//div[@class="mp-description-location"]/span[3]/text()')[0]

            #景区网友评分
            if selector.xpath('//div[@class="mp-description-comments"]/span[3]/span/text()'):
                self.jd_pingfen = selector.xpath('//div[@class="mp-description-comments"]/span[3]/span/text()')[0]
            #景区简介
            if selector.xpath('//div[@class="mp-charact-intro"]/div/p/text()'):
                self.jd_jianjie = selector.xpath('//div[@class="mp-charact-intro"]/div/p/text()')[0]
            #景区开放时间
            if selector.xpath('//div[@class="mp-charact-time"]/div/div[2]/p/text()'):
                self.jd_shijian = selector.xpath('//div[@class="mp-charact-time"]/div/div[2]/p')\
                [0].xpath('string(.)').replace('\r\n', '').replace(' ', '')
            #景区门票
            if selector.xpath('//div[@class="mp-description-price"]/span/text()'):
                self.jd_price = selector.xpath('//div[@class="mp-description-price"]/span')[0].xpath('string(.)').\
                    replace('\r\n', '').replace(' ','').replace('¥', '')
            #景区特色
            if selector.xpath('//div[@class="mp-charact-event"]'):
                self.jd_tese = ''
                self.jd_teseContent = ''
                for each1 in selector.xpath('//div[@class="mp-charact-event"]'):
                    if each1.xpath('div/div[2]/h3/text()'):
                        tese_name = each1.xpath('div/div[2]/h3/text()')[0]
                        self.jd_tese += tese_name + ','
                    # 特色说明
                    if each1.xpath('div/div[2]/p/text()'):
                        self.jd_teseContent += each1.xpath('div/div[2]/p/text()')[0] + ';'
                    #景点照片
                    if each1.xpath('div/img'):
                        img = each1.xpath('div/img/@src')[0]
                        #保存图片
                        # self.save_pic(img, tese_name)

            #其余信息
            if selector.xpath('//div[@class="mp-charact-littletips"][1]'):
                self.jd_ruyuan = '入园公告 :'
                ruyuan = selector.xpath('//div[@class="mp-charact-littletips"][1]/div/div[@class="mp-littletips-item"]')
                for each2 in ruyuan:
                    s1 = each2.xpath('div[1]/text()')[0]
                    s2 = each2.xpath('div[2]')[0].xpath('string(.)').replace('\r\n', '').replace(' ', '')
                    self.jd_ruyuan += s1 + ':' + s2
            if selector.xpath('//div[@class="mp-charact-littletips"][2]'):
                self.jd_tips = '小贴士 :'
                tips = selector.xpath('//div[@class="mp-charact-littletips"][2]/div/div[@class="mp-littletips-item"]')
                for each3 in tips:
                    d1 = each3.xpath('div[1]/text()')[0]
                    d2 = each3.xpath('div[2]')[0].xpath('string(.)').replace('\r\n', '').replace(' ', '')
                    self.jd_tips += d1 + ':' + d2

            #交通信息

            if selector.xpath('//div[@class="mp-traffic-transfer"]/div'):
                n = 1
                self.jd_traffic = ''
                while(True):
                    if selector.xpath('//div[@class="mp-traffic-transfer"]/div[' + str(n) + ']'):
                        title = selector.xpath('//div[@class="mp-traffic-transfer"]/div[' + str(n) + ']/text()')[0].\
                            replace('\n', '').replace('\r', '').replace(' ', '')
                        fangshi = selector.xpath('//div[@class="mp-traffic-transfer"]/div[' + str(n+1) + ']')[0]\
                            .xpath('string(.)').replace('\n', '').replace('\r', '').replace(' ', '')
                        self.jd_traffic += title + ': ' + fangshi + ';'
                    else:
                        break
                    n += 2
            self.get_jingweiduAndTel(response)
            self.save_txt()
        except Exception as e:
            print(e)
            self.item.append(item)

    def save_txt(self):
        text = str(self.jd_name) + str(self.column_split) + str(self.jd_star[0]) + str(self.column_split) +\
               str(self.jd_loc) + str(self.column_split) + str(self.jd_jianjie) + str(self.column_split) + \
               str(self.jd_shijian) + str(self.column_split) + str(self.jd_price) + str(self.column_split) + \
               str(self.jd_tese) + str(self.column_split) + str(self.jd_ruyuan) + str(self.column_split) + \
               str(self.jd_tips)+ str(self.column_split) + str(self.jd_traffic) + str(self.column_split) + \
               str(self.baidu_point) + str(self.column_split) + str(self.jd_Tel) + str(self.column_split)
        print(self.jd_name)
        with open('data.txt', 'a', encoding='utf-8') as f:
            f.writelines(text+ '\n')
    def save_pic(self, url, name):
        try:
            request.urlretrieve(url, filename=os.path.abspath('imgs') + '/' + self.jd_name + ',' + name + '.jpg')
        except :
            pass
    def get_commit(self):
        setUpSession.session.get_commit()
if __name__ == '__main__':
    print('选择项目: \n\t1.搜索抓取全部\n\t2.收缩抓取一条')
    INPUT_CHEKC = False
    while(True):
        iput = input('请选择: ')
        if iput is '1':
            dJson = dealWithJson()
            dJson.makeSession()

        elif iput is '2':
            gJD = getJingDianData()
            gJD.get_List()
        else:
            print('重新选择')
            INPUT_CHEKC = True
        if INPUT_CHEKC:
            continue
        else:
            break
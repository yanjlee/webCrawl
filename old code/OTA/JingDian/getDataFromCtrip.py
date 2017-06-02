# coding=utf8

'''
Info:
- author    : wangjiawei
- email     : wangjw@daqsoft.com.cn
- date      : 2017,03,08
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


from lxml import etree
from JingDian import USER_AGENT_LIST

#配置
class CtripSetting():
    ua = random.choice(USER_AGENT_LIST)
    host = 'piao.ctrip.com'
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
    list_a = open('list.txt', 'r', encoding='utf-8').readlines()
    #去'\n'
    list_b = []
    for i in list_a:
        list_b.append(i.replace('\n', ''))

#建立session,不需要登录就没有登录模块
class setUpSession(CtripSetting):
    session = requests.session()
    session.headers.update(CtripSetting.headers)
    def get_json(params):
        url = 'http://piao.ctrip.com/thingstodo-booking-bookingwebsite/api/AutoComplete'
        params = {
            'keyWords': params,
            'pageIndex': 1,
            'count': 15
        }
        return setUpSession.session.get(url, params=params).text

    def get_html(url):
        new_url = 'http://piao.ctrip.com' + url
        return setUpSession.session.get(new_url).text
        # return setUpSession.session.get('http://piao.ctrip.com/dest/t13720.html').text

#先搜索一遍,存放数据,再进行抓取
class getDataFromJson(setUpSession):
    def __init__(self, column_spilt='\u0001'):
        self.column_spilt = column_spilt
    #建立session
    def makeSession(self):
        js_list = loadInList.list_b
        for each in js_list:
            response = setUpSession.get_json(each)
            self.dealJson(response)
            time.sleep(3)

    #将数据放入文档
    def dealJson(self, content):
        if json.loads(content)['SearchList']:
            jdKw = json.loads(content)['SearchList'][0]['Name']
            jsDict = json.loads(content)['SearchList'][0]['Url']
            self.save(jdKw, jsDict)
    def save(self, name, url):
        text = '%s\u0001%s\u0001\n' %(name, url)
        with open('Json.txt', 'a', encoding='utf-8') as f:
            f.writelines(text)

#从json中提取url开始抓取景点数据
class getDataFromHtml(setUpSession):
    def __init__(self, column_split='\u0001', jd_name=None, jd_star=None, jd_loc=None, jd_time=None, jd_tese=None,
                 jd_jj=None, jd_jt=None, jd_point=None):
        self.column_split = column_split
        self.jd_name = jd_name
        self.jd_star = jd_star
        self.jd_loc = jd_loc
        self.jd_time = jd_time
        self.jd_tese = jd_tese
        self.jd_jj = jd_jj
        self.jd_jt = jd_jt
        self.jd_point = jd_point
        self.error = []
    def getInfoFromText(self):
        text = open('Json.txt', 'r', encoding='utf-8').readlines()
        for eachline in text:
            name = eachline.split(self.column_split)[0]
            url = eachline.split(self.column_split)[1]
            # print(name, url)
            self.makeSession(name, url)
            time.sleep(3)
        #抓取完毕
        for i in self.error:
            with open('erroe2.txt', 'a', encoding='utf-8') as f:
                f.writelines( i+ '\n')
    def makeSession(self, name, url):
        response = setUpSession.get_html(url)
        self.spyder(name, response, url)

    def spyder(self, name, response, url):
        try:
            selector = etree.HTML(response)
            if selector.xpath('//div[@class="media-right"]/h2/text()'):
                self.jd_name = selector.xpath('//div[@class="media-right"]/h2/text()')[0]
            else:
                self.jd_name = name
            if selector.xpath('//div[@class="media-right"]/span/text()'):
                self.jd_star = selector.xpath('//div[@class="media-right"]/span')[0].xpath('string(.)')
            if selector.xpath('//div[@class="media-right"]/ul/li[1]/span/text()'):
                self.jd_loc = selector.xpath('//div[@class="media-right"]/ul/li[1]/span/text()')[0].\
                    replace('\r\n', '').replace(' ', '')
            if selector.xpath('//div[@class="media-right"]/ul/li[2]/span/text()'):
                self.jd_time = selector.xpath('//div[@class="media-right"]/ul/li[2]/span/text()')[0].replace('\r\n', '')
            #景点特色
            if selector.xpath('//div[@id="J-Jdjj"]/div[2]/ul'):
                self.jd_tese = selector.xpath('//div[@id="J-Jdjj"]/div[2]/ul')[0].xpath('string(.)'). \
                    replace('\r\n', '').replace(' ', '')
            #景点简介
            if selector.xpath('//div[@id="J-Jdjj"]/div[2]/div/text()'):
                self.jd_jj = selector.xpath('//div[@id="J-Jdjj"]/div[2]/div')[0].xpath('string(.)').\
                    replace('\r\n', '').replace(' ', '')
            #交通指南
            if selector.xpath('//div[@id="J-Jtzn"]/div[@class="feature-traffic"]/text()'):
                self.jd_jt = selector.xpath('//div[@id="J-Jtzn"]/div[@class="feature-traffic"]')[0].xpath('string(.)').\
                    replace('\r\n', '').replace(' ', '')
            self.get_position(response)
            self.save()
        except Exception as e:
            print(e)
            self.error.append(name + '\u0001' + url)
    def get_position(self, response):
        try:
            text = re.findall('type="text/javascript" charset="utf-8"(.*?)minPrice:', response, re.S)[0]
            self.jd_point = re.findall('position: \'(.*?)\',', text, re.S)[0]
            return self.jd_point
        except Exception as e:
            print(e)

    def save(self):
        text = str(self.jd_name) + str(self.column_split) + str(self.jd_star) + str(self.column_split) + \
               str(self.jd_loc) + str(self.jd_jj) + str(self.column_split) + str(self.jd_time) + str(self.column_split) \
               + str(self.jd_tese) + str(self.column_split) + str(self.jd_jt) +\
                str(self.jd_point) + str(self.column_split)
        with open('data2.txt', 'a', encoding='utf-8') as f:
            print(self.jd_name)
            f.writelines(text + '\n')
if __name__ == '__main__':
    CHECK_CHOICE = True
    while(CHECK_CHOICE):
        try:
            print('携程景点抓取爬虫,请选择抓取项目:')
            print('\t1.搜索数据保存json')
            print('\t2.抓取景点信息')
            choice = input('请输入: ')
            if choice not in [1, 2]:
                raise Exception('请重新选择编号.')
                CHECK_CHOICE = False
        except Exception as e:
            print(e)
        if choice is '1':
            gdf = getDataFromJson()
            print('正在启动...')
            gdf.makeSession()
            CHECK_CHOICE = False
        elif choice is '2':
            gdh = getDataFromHtml()
            gdh.getInfoFromText()
            CHECK_CHOICE = False

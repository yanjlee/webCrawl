# coding=utf8

'''
Info:
- author    : wangjiawei
- email     : wangjw@daqsoft.com.cn
- date      : 2017,03,09
Update:
- name      :
- email     :
- date      :
'''


import requests
import random
import time
from lxml import etree
from JingDian import USER_AGENT_LIST


#配置
class TuniuSetting():
    ua = random.choice(USER_AGENT_LIST)
    headers1 = {
        'User-Agent': ua,
        'Host': 's.tuniu.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive'
    }
    headers2 = {
        'User-Agent': ua,
        'Host': 'menpiao.tuniu.com',
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


class setUpSession(TuniuSetting):
    session = requests.session()
    def get_search(params):
        url = 'http://s.tuniu.com/search_complex/ticket-cd-0-' + params + '/'
        r = setUpSession.session.get(url, headers=TuniuSetting.headers1, timeout=30)
        if r.status_code == 200:
            return r.text
        elif r.status_code == 302:
            return False
    def get_html(link):
        return setUpSession.session.get(link, headers=TuniuSetting.headers2, timeout=30).text

#先搜索一遍,存放数据,再进行抓取
class getDataFromSearch(setUpSession):
    def __init__(self, column_spilt='\u0001', jd_name=None, jd_info=None, jd_price=None, jd_shijian=None, jd_tese=None,
                 jd_jj=None, jd_jd=None, jd_kf=None, jd_zc=None, jd_fy=None, jd_jt=None):
        self.column_spilt = column_spilt
        self.jd_name = jd_name
        self.jd_info = jd_info
        self.jd_price = jd_price
        self.jd_shijian = jd_shijian
        self.jd_tese = jd_tese
        self.jd_jj = jd_jj
        self.jd_jd = jd_jd
        self.jd_kf = jd_kf
        self.jd_zc = jd_zc
        self.jd_fy = jd_fy
        self.jd_jt = jd_jt
        self.error = []
    #建立session
    def makeSession(self):
        js_list = loadInList.list_b
        num = len(js_list)
        for i in range(num):
            print(i + 1)
            response = setUpSession.get_search(js_list[i + 1])
            if response:
                self.dealResponse(response, js_list[i + 1])
                time.sleep(3)
                break
    #需要一个验证码模块
    def dealResponse(self, content, name):
        selector = etree.HTML(content)
        if selector.xpath('//div[@class="theinfo ticket clearfix"]'):
            self.deal_redicted(content, name)
        elif selector.xpath('/html/head/title/text()') is '访问速度过快 - 途牛旅游网':
            self.deal_capcha(content)
        else:
            pass
    #处理验证码
    def deal_capcha(self, content):
        # selector = etree.HTML(content)
        # post_url = selector.xpath('//form/@action')[0]
        # input1 = selector.xpath('//form/input[1]/@value')[0]
        # input2 = selector.xpath('//form/input[2]/@value')[0]
        # capcha_url = 'http://s.tuniu.com/?t=limitRequest/code'
        # print('请输入验证码:')
        # ipu = input('点击: '+ capcha_url)
        pass
    def deal_redicted(self, content, name):
        try:
            selector = etree.HTML(content)
            # print(content)
            url = selector.xpath('//div[@class="thelist an_mo"]/ul/li[1]/div/div[2]/p/a/@href')[0]
            self.getData(setUpSession.get_html(url))
        except Exception as e:
            print(e)
            self.error.append(name)
    #抓取页面数据
    def getData(self, content):
        selector = etree.HTML(content)
        self.jd_name = selector.xpath('//div[@class="tp_title clearfix"]/div[1]/div/h1/text()')[0].replace('\t', '')
        if selector.xpath('//div[@class="tp_title clearfix"]/div[1]/p/text()'):
            self.jd_info = selector.xpath('//div[@class="tp_title clearfix"]/div[1]/p/text()')[0]
        if selector.xpath('//div[@class="tp_title clearfix"]/div[2]/div[1]/span/text()'):
            self.jd_price = selector.xpath('//div[@class="tp_title clearfix"]/div[2]/div[1]/span/text()')[0]
        #特色
        if selector.xpath('//div[@class="pkg-detail-infor graybg_color"]/div[1]/p/text()'):
            self.jd_shijian = selector.xpath('//div[@class="pkg-detail-infor graybg_color"]/div[1]/p')[0].xpath('string(.)')
        if selector.xpath('//div[@class="pkg-detail-infor graybg_color"]/div[2]/div/div/p/text()'):
            self.jd_tese = selector.xpath('//div[@class="pkg-detail-infor graybg_color"]/div[2]/div/div')[0].xpath('string(.)').replace('\r\n', '').replace('\t', '')
        #简介及景点
        if selector.xpath('//div[@class="pkg-detail-box"]/div[1]/div/div/dl/dd/text()'):
            self.jd_jj = selector.xpath('//div[@class="pkg-detail-box"]/div[1]/div/div/dl/dd/text()')[0]
        #景点
        if selector.xpath('//div[@class="pkg-detail-box"]/div[1]/div/div/p'):
            con = selector.xpath('//div[@class="pkg-detail-box"]/div[1]/div/div/p')
            self.jd_jd = ''
            for each in con:
                if each.xpath('strong/text()'):
                    title = each.xpath('strong/text()')[0].replace('★', '')
                    text = each.xpath('text()')[0]
                    self.jd_jd += title + ': ' + text + ';'
        #开放时间
        if selector.xpath('//div[@class="order_detail_imfor"]/dl[1]/dd/text()'):
            self.jd_kf = selector.xpath('//div[@class="order_detail_imfor"]/dl[1]/dd')[0].\
                xpath('string(.)').replace('\n', '')
        #特殊政策
        if selector.xpath('//div[@class="order_detail_imfor"]/dl[5]/dd/text()'):
            self.jd_zc = selector.xpath('//div[@class="order_detail_imfor"]/dl[5]/dd')[0].\
                xpath('string(.)').replace('\n', '')
        #费用说明
        if selector.xpath('//div[@class="order_detail_imfor"]/dl[6]/dd/text()'):
            self.jd_fy = selector.xpath('//div[@class="order_detail_imfor"]/dl[6]/dd')[0].\
                xpath('string(.)').replace('\n', '')
        #交通
        if selector.xpath('//div[@class="pkg-detail-infor"]/div//ul/li[1]/p/text()'):
            self.jd_jt = selector.xpath('//div[@class="pkg-detail-infor"]/div//ul/li[1]/p/text()')[0].\
                replace('\r\n', '')
            print(selector.xpath('//div[@class="pkg-detail-infor"]/div//ul/li[1]/p/text()'))
        # print(self.jd_info)
        self.save()

    def save(self):
        text = str(self.jd_name) + str(self.column_spilt) + str(self.jd_info) + str(self.column_spilt) +\
            str(self.jd_price) + str(self.column_spilt) + str(self.jd_kf) + str(self.column_spilt) + \
            str(self.jd_zc) + str(self.column_spilt) + str(self.jd_jj) + str(self.column_spilt) + \
            str(self.jd_tese)+ str(self.column_spilt) + str(self.jd_jd) + str(self.column_spilt) + \
            str(self.jd_shijian) + str(self.jd_fy) + str(self.column_spilt) + str(self.jd_jt) + str(self.column_spilt)
        with open('dataTuniu.txt', 'a', encoding='utf-8') as f:
            print(self.jd_name)
            f.writelines(text + '\n')



if __name__ == '__main__':
    c = getDataFromSearch()
    c.makeSession()
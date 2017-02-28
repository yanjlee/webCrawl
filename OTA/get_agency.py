# coding=utf8
'''
- author : 'wangjiawei'
- email  : 'forme.wjw@aliyun.com'
- date   : '2017.2.28'
Update
- name   : ''
- email  : ''
- date   : ''
'''

import re
import requests
import random
import time
# from . import user_agent_list
from lxml import etree
from urllib import request


class allAgency():
    def __init__(self):
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        self.headers = {
            'User-Agent': random.choice(user_agent_list),
            'Host': 'lxs.cncn.com',
            'Referer': 'http://sichuan.cncn.com/lvxingshe/'
        }
        self.headers.update()
        self.session = requests.session()
        #建立保存信息的文本
        open('data.txt', 'w', encoding='utf-8')
    def setupsession(self):
        url = 'http://lxs.cncn.com/'
        self.province_urls = {}
        selector = etree.HTML(self.session.get(url, headers=self.headers).content)
        content = selector.xpath('//ul[@class="prov"]/li')
        for each in content:
            url = each.xpath('a/@href')[0]
            province_name = each.xpath('a/text()')[0]
            self.province_urls[province_name] = url
        return self.get_eachProvince_agency(self.province_urls)

    def get_eachProvince_agency(self, province_urls):
        for key in province_urls.keys():
            # 这里开始写入省份
            f = open('data.txt', 'a')
            text = '省份 :' + key + '\n'
            f.writelines(text)
            self.get_pages(key, province_urls[key])
            time.sleep(2)
    #作为翻页而存在的
    def get_pages(self, key, url):
        selector = etree.HTML(self.session.get(url).text)
        pages = selector.xpath('//div[@class="page"]/div/span[@class="text"]/text()')[0]
        page_num = re.findall('\d{1,2}', pages, re.S)[0]
        for i in range(int(page_num)):
            p_url = url + '/index' + str(i+1) + '.htm'
            # print(p_url)
            self.get_agency_data(key, p_url)

    #获取旅行社的名称,url,许可证,主营业务,img地址
    def get_agency_data(self, key, url):
        time.sleep(2)
        selector = etree.HTML(self.session.get(url).text)
        content = selector.xpath('//div[@class="lxs_list"]/div')
        for each in content:
            name = each.xpath('div[2]/h3/a/text()')[0]
            url = each.xpath('div[2]/h3/a/@href')[0]
            xukezheng = each.xpath('div[2]/ul/li[1]/text()')[0]
            zhuying = each.xpath('div[2]/ul/li[2]')[0].xpath('string(.)')
            img = each.xpath('div[1]/a/img/@data-original')[0]
            self.getEachAgency_data(url, name, xukezheng, zhuying, img, key)


    def getEachAgency_data(self, url, name, xkz, zy, img, key):
        print('录入数据' + key, name)
        time.sleep(2)
        url_data = url + '-contact.html'
        selector = etree.HTML(self.session.get(url_data).text)
        c_name = selector.xpath('//div[@class="box950"]/h4/text()')[0]
        address_info = selector.xpath('//div[@class="box950"]/div[@class="address_info"]')[0].xpath('string(.)')
        if selector.xpath('//div[@class="box950"]/div[@class="lxs_zizhi"]/span[1]/a/@href'):
            xkz = selector.xpath('//div[@class="box950"]/div[@class="lxs_zizhi"]/span[1]/a/@href')[0]
        else:
            xkz = ''
        kf = selector.xpath('//div[@class="box950"]/div[@class="line_kefu"]/ul/li')
        kefu = ''
        for each in kf:
            if each.xpath('strong/text()'):
                kf_name = each.xpath('strong/text()')[0]
            else:
                kf_name = ''
            if each.xpath('p/text()'):
                tel = each.xpath('p/text()')[0]
            else:
                tel = ''
            if each.xpath('div[@class="qq"]/a/@href'):
                qq = each.xpath('div[@class="qq"]/a/@href')[0]
            else:
                qq = ''
            kefu += kf_name + ':' + tel + ', qq:' + qq + ';'
        #开始写入
        text = '旅行社名称 :' + name + ', 许可证号 :' + xkz + ', 主营业务 :' + zy + ',' +\
               address_info + ', 客服 :' + kefu + '\n'
        f = open('data.txt', 'a')
        f.writelines(text)

        #储存图片
        if xkz is not '':
            self.save_img(img, xkz, c_name)
        else:
            self.save_imgWithoutXKZ(img, c_name)
    def save_img(self, img, xkz, name):
        time.sleep(2)
        selector = etree.HTML(self.session.get(xkz).content)
        img_url = selector.xpath('//div[@id="conten"]/div/a/@href')[0]
        request.urlretrieve(img_url, filename='imgs/' + name + '许可证.jpg')
        request.urlretrieve(img, filename='imgs/' + name + '图标.jpg')

    def save_imgWithoutXKZ(self, img, name):
        time.sleep(2)
        request.urlretrieve(img, filename='imgs/' + name + '图标.jpg')

if __name__ == '__main__':
    c = allAgency()
    c.setupsession()
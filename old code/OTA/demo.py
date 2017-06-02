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

import requests
import time
import os
import random
from . import user_agent_list
from lxml import etree

class demoSetting():
    url = ''
    #构建headers
    host = ''
    referer = ''
    headers= {
        'User-Agent': random.choice(user_agent_list),
        'host': host,
        'referer': referer,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    #用于GET请求时构造url时对一下字符的替换
    quote = {
        ':': '%253A',
        '/': '%252F',
        '?': '%253F',
        '=': '%253D',
        '&': '%2526'
    }
    #url需要编码
    def url_quote(self, url):
        url_quote = url
        for source, target in demoSetting.quote.items():
            url_quote.replace(source, target)
        return url_quote
    #url不需要编码
    def url_unquote(self, url):
        url_quote = url

class demoLoginer():
    def __init__(self, username='', passwd=''):
        self.input = input
        self.username = username
        self.passwd = passwd
        #构建session
        self.session = requests.session()
        #更新headers
        self.session.headers.update(demoSetting.headers)
        #更新cookies
    def login(self):
        #向爬虫加载cookies
        self.session.cookies.update(self.session.get('登陆页面url'))
        post_data = {
            'username': self.username,
            'password': self.passwd
        }
        #判断是否有验证码
        selector = etree.HTML(self.session.get('登陆页面url').content)
        #找到验证码的标签
        content = selector.xpath()
        if content:
            print('需要验证码,请输入验证码')
            self.get_capcha_click(self.session.get('登陆页面url').content)
            capcha = input()
            post_data['capcha'] = capcha
        else:
            print('不需要验证码')
        #登陆
        r = self.session.post('post登陆数据url')
        #更新cookies
        self.session.cookies.update(r.cookies)
    #获取验证码url，两种方法，简单的解析出验证码url点击并查看，一种是推导出url并保存图片
    def get_capcha_click(self, content):
        selector = etree.HTML(content)
        #解析出capcha的url
        return print('解析出的url')
    def get_capcah_construct(self):
        #capcha根据时间末尾乘数可能发生变化
        t = str(int(time.time())*1000)
        #构造url
        capcha_url = '' + t
        #保存图片
        r = self.session.get(capcha_url)
        #创建文件夹并保存
        img_dir = os.path.abspath('captcha/')
        img_name = os.path.abspath('captcha/' + t + '.jpg')
        return print('打开' + img_dir + '并查看验证码')

    #验证登陆
    def isLogin(self):
        status_codes = self.session.get('验证url', allow_redricts=False).status_code
        if status_codes is str(200):
            return True
        else:
            return False
#获取数据
class demoSession():
    url_1 = ''
    url_2 = ''
    url_3 = ''


if __name__ == '__main__':
    pass
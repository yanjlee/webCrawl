# coding=utf8


'''
Info:
- author    : wangjiawei
- email     : wangjw@daqsoft.com.cn
- date      : 2017,03,10
Update:
- name      :
- email     :
- date      :
'''


import re
import time
from lxml import etree
from xpinyin import Pinyin
from JingDian.sessions import makeSession
from JingDian.spyder import BaiduSpyder

#导入数据列表
class loadInData():
    list_a = open('data/list.txt', 'r', encoding='utf-8').readlines()
    # 去'\n'
    list_b = []
    for i in list_a:
        list_b.append(i.replace('\n', ''))



#数据抓取模块
class getDataFromBaidu():
    def __init__(self):
        self.host = 'lvyou.baidu.com'
    #程序开始
    def run(self):
        return self.useList()
    #获得数据列表
    def useList(self):
        num = len(loadInData.list_b)
        for i in range(num):
            print(i + 1)
            self.do_clear(loadInData.list_b[i])
            time.sleep(5)

    #去尾巴
    def do_clear(self, content):
        if re.findall('(.*?)公园|景区|游览区|风景区', content, re.S):
            text = re.findall('(.*?)公园|景区|游览区|风景区', content, re.S)[0]
            self.convert2PY(text)
        else:
            self.convert2PY(content)
    #将中文转化成拼音
    def convert2PY(self, params):
        p = Pinyin()
        py = p.get_pinyin(params, '')
        self.setUpSessions(py)

    #调用makeSession,创建session
    def setUpSessions(self, params):
        ms = makeSession()
        response = ms.get_baidu_html(self.host, params)
        if response:
            self.dealResponse(response)

    #处理返回,如果是空,如果有数据
    def dealResponse(self, response):
        selector = etree.HTML(response)
        if selector.xpath('//body[@class="theme-new-blue theme-new-blue-nosync "]'):
            #实例化百度爬虫,并传入response
            bd = BaiduSpyder()
            bd.getResponse(response)


if __name__ == '__main__':
    g = getDataFromBaidu()
    g.run()
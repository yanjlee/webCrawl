# -*-coding:utf8 -*-

import requests
import MySQLdb
from lxml import etree
import sys



reload(sys)
sys.setdefaultencoding('utf8')

class tongji():
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
    def setup(self):
        self.cur = self.conn.cursor()
        html = open('tongjirenshu').read()
        selector = etree.HTML(html.decode('utf-8'))
        self.getdata(selector)
        print '抓取完毕'
        self.conn.close()

    def getdata(self, selector):
        content = selector.xpath('//table/tbody/tr')
        for each_info in content:
            if each_info.xpath('td[1]/strong/text()'):
                continue
            else:
                province = each_info.xpath('td[1]/text()')[0].replace('\n', '')
                if each_info.xpath('td[2]/a/text()'):
                    num = each_info.xpath('td[2]/a/text()')[0].replace('\n', '')
                else : num = ''
                if each_info.xpath('td[3]/text()'):
                    biqunian = each_info.xpath('td[3]/text()')[0].replace('\n', '')
                else : biqunian = ''
                if each_info.xpath('td[4]/a/text()'):
                    tongkao = each_info.xpath('td[4]/a/text()')[0].replace('\n', '')
                else : tongkao = ''
                if each_info.xpath('td[5]/text()'):
                    tong_qunian = each_info.xpath('td[5]/text()')[0].replace('\n', '')
                else : tong_qunian = ''
                if each_info.xpath('td[6]/a/text()'):
                    nian15 = each_info.xpath('td[6]/a/text()')[0].replace('\n', '')
                if each_info.xpath('td[7]/text()'):
                    nian14 = each_info.xpath('td[7]/text()')[0].replace('\n', '')
                if each_info.xpath('td[8]/text()'):
                    nian13 = each_info.xpath('td[7]/text()')[0].replace('\n', '')
                if each_info.xpath('td[9]/text()'):
                    nian12 = each_info.xpath('td[7]/text()')[0].replace('\n', '')
                if each_info.xpath('td[10]/text()'):
                    nian11 = each_info.xpath('td[7]/text()')[0].replace('\n', '')
                if each_info.xpath('td[11]/text()'):
                    nian10 = each_info.xpath('td[7]/text()')[0].replace('\n', '')
                SQL = 'insert into tongjirenshu(省份,2016年人数,总数相比15年,16年统考生人数,统考生相比15年,2015年人数,2014年人数' \
                      ',2013年人数,2012年人数,2011年人数,2010年人数)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'' \
                      ',\'%s\',\'%s\',\'%s\',\'%s\')' %(province, num, biqunian, tongkao, tong_qunian, nian15, nian14,
                                                        nian13, nian12, nian11, nian10)
                self.cur.execute(SQL)
                self.conn.commit()



if __name__ == '__main__':
    c = tongji()
    c.setup()
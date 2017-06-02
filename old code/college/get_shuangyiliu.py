# -*-coding:utf8 -*-

import requests
import MySQLdb
from lxml import etree
import sys



reload(sys)
sys.setdefaultencoding('utf8')

class shuangyiliu():
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
    def setup(self):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Host': 'learning.sohu.com'
        }
        url = 'http://learning.sohu.com/20160725/n460962725.shtml'
        selector = etree.HTML(requests.get(url, headers=headers).content)
        for i in range(8):
            self.getdata(i+1, selector)
            self.conn.commit()
    def getdata(self, i, selector):
        content = selector.xpath('//*[@id="contentText"]/table['+ str(i) + ']/tbody/tr')
        for each_info in content:
            if  each_info.xpath('td[1]/span/strong[2]/text()'):
                continue
            if  each_info.xpath('td[1]/span/strong/text()'):
                num = each_info.xpath('td[1]/span/strong/text()')[0]
            if  each_info.xpath('td[2]/span/strong/text()'):
                schoolname = each_info.xpath('td[2]/span/strong/text()')[0]
            if each_info.xpath('td[3]/span/strong/text()'):
                A = each_info.xpath('td[3]/span/strong/text()')[0]
            if each_info.xpath('td[4]/span/strong/text()'):
                B = each_info.xpath('td[4]/span/strong/text()')[0]
            if each_info.xpath('td[5]/span/strong/text()'):
                C = each_info.xpath('td[5]/span/strong/text()')[0]

            SQL = 'insert into shuangyiliu (总所数和编号,大学名称,A类学科,B类学科,C类学科)values' \
                  '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'% (num, schoolname, A, B, C)
            self.cur.execute(SQL)



if __name__ == '__main__':
    s = shuangyiliu()
    s.setup()
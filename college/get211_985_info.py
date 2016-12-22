# -*-coding:utf-8 -*-

from lxml import etree
import MySQLdb
import sys



reload(sys)
sys.setdefaultencoding('utf8')


class the_985_211_info():
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
    def setupconnect(self):
        self.cur = self.conn.cursor()
        self.get_958()
        self.get_211()
        print '抓取完毕'
        self.conn.close()

    def get_958(self):
        html = open('985_211').read()
        selector = etree.HTML(html.decode('utf-8'))
        content_985 = selector.xpath('//table[2]/tbody/tr')
        for each_info in content_985:
            name = each_info.xpath('td[1]/a/@title')[0]
            if each_info.xpath('td[2]/span/text()'):
                time = each_info.xpath('td[2]/span/text()')[0]
            else: time = ''
            area = each_info.xpath('td[3]/a/span/text()')[0]
            membership = each_info.xpath('td[4]/a/@title')[0]
            SQL = 'insert into 985_info(名称,签约时间,所在地,所属部门)values(\'%s\',\'%s\',\'%s\',\'%s\')' \
                  ''%(name, time, area, membership)
            self.cur.execute(SQL)
        self.conn.commit()

    def get_211(self):
        html = open('985_211').read()
        selector = etree.HTML(html.decode('utf-8'))
        content_211 = selector.xpath('//table[1]/tbody/tr')
        for each_info in content_211:
            name = each_info.xpath('td[2]/p/span/span/text()')[0]
            time = each_info.xpath('td[3]/p/span/span/text()')[0]
            if each_info.xpath('td[4]/p/span/span/text()'):
                membership = each_info.xpath('td[4]/p/span/span/text()')[0]
            elif each_info.xpath('td[4]/p/span/text()'):
                membership = each_info.xpath('td[4]/p/span/text()')[0]
            type = each_info.xpath('td[5]/p/span/text()')[0]
            s_time = each_info.xpath('td[6]/p/span/span/text()')[0]
            SQL = 'insert into 211_info(大学名称,建校时间,隶属关系,教研类型,立项时间)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                  '' % (name, time, membership, type, s_time)
            self.cur.execute(SQL)
        self.conn.commit()

if __name__ == '__main__':
    t = the_985_211_info()
    t.setupconnect()
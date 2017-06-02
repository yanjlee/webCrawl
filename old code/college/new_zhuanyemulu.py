# -*-coding:utf8 -*-

import requests
import time
import random
import MySQLdb
from lxml import etree
import sys
reload(sys)
sys.setrecursionlimit(2000000)

sys.setdefaultencoding('utf-8')


class zhuanyedaquan():
    def __init__(self):
        self.user_agent_list = [
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

        self.headers = {'User-Agent': random.choice(self.user_agent_list),
                        'Host': 'www.zjut.cc'}
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
    def setupsession_benke(self, s):
        url_benke = 'http://www.zjut.cc/zhuanye/benke/'
        r = self.session.get(url_benke)
        self.session.cookies.update(r.cookies)
        return self.get1stUrls(r.content, s)

    def setupsession_zhuanke(self, s):
        url_benke = 'http://www.zjut.cc/zhuanye/zhuanke/'
        r = self.session.get(url_benke)
        self.session.cookies.update(r.cookies)
        return self.get1stUrls(r.content, s)

    def get1stUrls(self, content, s):
        selector = etree.HTML(content)
        content = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="list-group"]/a')
        for each in content:
            name_1 = each.xpath('text()')[0]
            url_1 = each.xpath('@href')[0]
            self.get2ndUrls(name_1, url_1, s)
            time.sleep(2)

        self.conn.close()
    def get2ndUrls(self, name_1, url_1, s):
        selector = etree.HTML(self.session.get(url_1).content)
        content = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="list-group"]/a')
        for each in content:
            name_2 = each.xpath('text()')[0]
            url_2 = each.xpath('@href')[0]
            self.get3rdUrls(name_1, name_2, url_2, s)
            time.sleep(2)
    def get3rdUrls(self, name_1, name_2, url_2, s):
        selector = etree.HTML(self.session.get(url_2).content)
        content = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="list-group"]/a')
        for each in content:
            name_3 = each.xpath('text()')[0]
            url_3 = each.xpath('@href')[0]
            if s == '本科':
                self.get4thUrls_ben(name_1, name_2, name_3, url_3, s)
            elif s == '专科':
                self.get4thUrls_zhuan(name_1, name_2, name_3, url_3, s)
            time.sleep(2)
    def get4thUrls_ben(self, name_1, name_2, name_3, url_3, s):
        selector = etree.HTML(self.session.get(url_3).content)
        type = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]'
                               '/table/tr/td[2]/text()')[0]
        time = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]'
                            '/table/tr/td[3]/text()')[0]
        sql = 'insert into new_专业目录(层次,一级学科,二级学科,三级学科,专业代码,授予学位,修业年限)values' \
                '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (s, name_1, name_2, name_3, id, type, time)
        print '录入', name_1, name_2, name_3
        self.cur.execute(sql)
        self.conn.commit()

    def get4thUrls_zhuan(self, name_1, name_2, name_3, url_3, s):
        selector = etree.HTML(self.session.get(url_3).content)
        # if selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]/table'):
        # content = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]/table')
        if selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]'
                          '/table/tr/td[1]/text()'):
            id = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]'
                                '/table/tr/td[1]/text()')[0]
            if selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]'
                              '/table/tr/td[2]/text()'):
                time = selector.xpath('//div[@class="row"]/div[@class="col-md-8"]/div[@class="table-responsive"]'
                                        '/table/tr/td[2]/text()')[0]
                sql = 'insert into new_专业目录(层次,一级学科,二级学科,三级学科,专业代码,修业年限)values' \
                        '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (s, name_1, name_2, name_3, id, time)
                print '录入', name_1, name_2, name_3
                self.cur.execute(sql)
                self.conn.commit()
            else:
                sql = 'insert into new_专业目录(层次,一级学科,二级学科,三级学科,专业代码)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (s, name_1, name_2, name_3, id)
                print '录入', name_1, name_2, name_3
                self.cur.execute(sql)
                self.conn.commit()
        else:
            sql = 'insert into new_专业目录(层次,一级学科,二级学科,三级学科)values' \
                  '(\'%s\',\'%s\',\'%s\',\'%s\')' % (s, name_1, name_2, name_3)
            print '录入', name_1, name_2, name_3
            self.cur.execute(sql)
            self.conn.commit()

if __name__ == '__main__':
    z = zhuanyedaquan()
    z.setupsession_benke('本科')
    z.setupsession_zhuanke('专科')
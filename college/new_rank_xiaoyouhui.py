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


class feeOfEachCollege():
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

    def setupsession(self):
        url = 'http://www.zjut.cc/article-18606-1.html'
        r = self.session.get(url)
        self.session.cookies.update(r.cookies)
        return self.getEachProvinceUrls(r.content)

    def getEachProvinceUrls(self, content):
        selector = etree.HTML(content)
        content = selector.xpath('//*[@id="article_content"]/ul/li')
        for each in content:
            link = each.xpath('a/@href')[0]
            prov = each.xpath('a/text()')[0].replace('校友会2016大学排行榜—2016年', '').replace('的大学排名', '')
            self.getEachCollege(link, prov)
            time.sleep(3)

        print '抓取结束'
        self.conn.close()
    def getEachCollege(self, link, prov):
        selector = etree.HTML(self.session.get(link).content)
        content = selector.xpath('//*[@id="article_content"]/div')
        for each in content:
            url = each.xpath('div/h4/a/@href')[0]
            name = each.xpath('div/h4/a/text()')[0]
            self.getData(url, name, prov)

    def getData(self, url, name, prov):
        selector = etree.HTML(self.session.get(url).content)
        content = selector.xpath('//*[@id="article_content"]/div[4]/table/tbody/tr')
        for each in content:
            year = each.xpath('td[1]/text()')[0]
            rank = each.xpath('td[2]/text()')[0]
            sql = 'insert into new_大学排名_校友会(省份,院校名称,年份,排名)values(\'%s\',\'%s\',\'%s\',\'%s\')'\
                  % (prov, name, year, rank)

            self.cur.execute(sql)
        self.conn.commit()

if __name__ == '__main__':
    f = feeOfEachCollege()
    f.setupsession()

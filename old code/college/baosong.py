# -*-coding:utf8 -*-

import requests
import time
import random
import MySQLdb
from lxml import etree
import sys
reload(sys)


sys.setdefaultencoding('utf-8')

class baosong():
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

        self.headers = {'Host': 'gaokao.chsi.com.cn',
                        'User-Agent': random.choice(self.user_agent_list)
                        }
        self.session = requests.session()

    def setupsession(self):
        r = self.session.get('http://gaokao.chsi.com.cn/zsgs/bsszgmd--method-listByJxmc,year-2016.dhtml'
                            , headers=self.headers, timeout=10)
        # 建立mysql链接
        self.conn = MySQLdb.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='454647',
                db='college_info',
                charset="utf8"
                )
        self.cur = self.conn.cursor()
        #创建表
        # SQL = 'create table 保送生信息(id int auto_increment primary key,姓名 nvarchar(20),性别 nvarchar(10),' \
        #             '所在省市 nvarchar(20),毕业学校 nvarchar(100), 备注 nvarchar(200));'
        # self.cur.execute(SQL)
        # self.conn.commit()
        return self.getUrl(r.content)

    def getUrl(self, content):
        selector = etree.HTML(content)
        content = selector.xpath('//table[@class="mrg_auto bg_color03"]/tr')
        for each in content:
            if each.xpath('td/a'):
                url = each.xpath('td/a/@href')[0]
                title = each.xpath('td/a/text()')[0]
                self.geturls(url, title)

        self.conn.commit()

    def geturls(self, url, title):
        Url = 'http://gaokao.chsi.com.cn' + url
        selector = etree.HTML(self.session.get(Url).content)
        if selector.xpath('//div[@class="clearfix"]/ul/li'):
            p_url = selector.xpath('//div[@class="clearfix"]/ul/li')
            for each in p_url:
                link = each.xpath('a/@href')[0]
                # province = each.xpath('a/text()')[0]
                self.getdata(link, title)
                time.sleep(2)
        else:
            self.getdata(url, title)

    def getdata(self, url, title):
        URL = 'http://gaokao.chsi.com.cn' + url
        selector = etree.HTML(self.session.get(URL).content)
        ex = selector.xpath('/html/body/div[2]/h3/text()')[0]
        content = selector.xpath('//*[@id="YKTabCon2_10"]/tr')
        for each in content:
            if each.xpath('td[@width="15%"]'):
                continue
            else:
                name = each.xpath('td[1]/text()')[0]
                sex = each.xpath('td[2]/text()')[0]
                belong = each.xpath('td[3]/text()')[0]
                school = each.xpath('td[4]/text()')[0]
                sql = 'insert into 保送生信息(姓名,性别,所在省市,毕业学校,备注)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(name, sex, belong, school, ex)
                print sql
                self.cur.execute(sql)
        self.conn.commit()

if __name__ == '__main__':
    b = baosong()
    b.setupsession()
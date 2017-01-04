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

class getAllCollege():
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 "
            "(X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 "
            "(Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 "
            "(Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        self.headers = {'User-Agent': random.choice(self.user_agent_list)}
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
        self.prop_name = []
        self.url = []
        self.n = 0
    def setupsession(self):
        url = 'http://college.zjut.cc/'
        headers = {
            'Host': 'college.zjut.cc',
            'Referer': 'http://www.zjut.cc/'
        }
        #添加cookies信息
        r = self.session.get(url, headers=headers)
        self.session.cookies.update(r.cookies)
        return self.getUrls(r.content)
    def getUrls(self, content):
        if len(self.prop_name) is not 0:
            self.ex()
        else:
            selector = etree.HTML(content)
            property = selector.xpath('///ul[@class="nav nav-tabs"]/li')
            for each_property in property:
                property_name = each_property.xpath('a/text()')[0]
                link = each_property.xpath('a/@href')[0].replace('#', '')
                # 依据 link找到对应的div,来抓取对应的内容.
                thePath = '//div[@class="tab-content"]/div[@id="' + link +'"]'
                # content = selector.xpath(thePath)
                #一共有31个省
                for i in range(31):
                    # prov_name = selector.xpath(thePath + '/h3[' + str(i+1) + ']/text()')[0]
                    content = selector.xpath(thePath + '/ul[' + str(i+1) + ']/li')
                    for each in content:
                        school_name = each.xpath('a/text()')[0]
                        school_url = each.xpath('a/@href')[0]
                        #转跳录入环节
                        self.insertData(property_name, school_url)

            #处理失效链接
            if self.prop_name:
                self.ex()
            else:
                self.conn.close()

    def insertData(self, property_name, school_url):
        try:
            headers = {
                'Host': 'college.zjut.cc',
                'Referer': 'http://college.zjut.cc/'
            }
            selector = etree.HTML(self.session.get(school_url, headers=headers).content)
            # content = selector.xpath('//table[@class="table table-bordered"]/tr')
            name = selector.xpath('//table[@class="table table-bordered"]/tr[1]/td/text()')[0]
            provence = selector.xpath('//table[@class="table table-bordered"]/tr[3]/td/a/text()')[0]
            if selector.xpath('//table[@class="table table-bordered"]/tr[4]/td/a/text()'):
                type = selector.xpath('//table[@class="table table-bordered"]/tr[4]/td/a/text()')[0]
            else:
                type = ''
            cengci = selector.xpath('//table[@class="table table-bordered"]/tr[5]/td/a/text()')[0]
            zhongdian = selector.xpath('//table[@class="table table-bordered"]/tr[6]/td/text()')[0]
            yuanshi = selector.xpath('//table[@class="table table-bordered"]/tr[7]/td/text()')[0]
            boshidian = selector.xpath('//table[@class="table table-bordered"]/tr[8]/td/text()')[0]
            shuoshidian = selector.xpath('//table[@class="table table-bordered"]/tr[9]/td/text()')[0]
            if selector.xpath('//table[@class="table table-bordered"]/tr[10]/td/text()'):
                tel = selector.xpath('//table[@class="table table-bordered"]/tr[10]/td/text()')[0]
            else:
                tel = ''
            if selector.xpath('//table[@class="table table-bordered"]/tr[11]/td/text()'):
                address = selector.xpath('//table[@class="table table-bordered"]/tr[11]/td/text()')[0]\
                    .replace(' ...', '')
            else:
                address = ''
            print '录入', self.n, property_name, provence, name, '\n'
            sql = 'insert into new_全国高校基本数据 (性质,院校名称,所在省市,办学类型,办学层次,重点学科,院士,博士点,硕士点,联系电话,' \
                  '通讯地址,url)values' \
                  '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                % (property_name, name, provence, type, cengci, zhongdian,
                  yuanshi, boshidian, shuoshidian, tel, address, school_url)
            self.cur.execute(sql)
            self.conn.commit()
            self.n += 1
        except:
            print '录入数据错误',provence, name, '\n'
            self.prop_name.append(property_name)
            self.url.append(school_url)

    def ex(self):
        self.n = 0
        if self.prop_name:
            for i in range(len(self.prop_name)):
                print '补充录入第', i, '个'
                self.insertData(self.prop_name[i], self.url[i])

            self.prop_name = []
            self.url = []
            return self.setupsession()
        else:
            print '录入结束'
            self.conn.clse()


if __name__ == '__main__':
    c = getAllCollege()
    c.setupsession()


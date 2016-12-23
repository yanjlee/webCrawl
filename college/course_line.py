# -*- coding:utf-8 -*-

import requests
import MySQLdb
import random
import time
from lxml import etree
import re
import sys
reload(sys)


sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000000)


class course_line():
    def __init__(self):
        self.user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1", \
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]

        self.headers = {'Host': 'gkcx.eol.cn',
                        'User-Agent': random.choice(self.user_agent_list)
                        }
        self.session = requests.session()

    def setupsession(self):
        try:
            r = self.session.get('http://gkcx.eol.cn/',headers=self.headers, timeout= 10)
            cookies = r.cookies
            self.session.cookies.update(cookies)
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
            self.cur.execute('select count(*) from all_college')
            self.total_school = self.cur.fetchone()[0]
            return self.getUrl()
        except:
            print 'set up session 这里错误'



    def getUrl(self):
        self.wrong_url = []
        for i in range(int(self.total_school)):
            print '第', i + 1, '所学校'
            self.cur.execute("select schoolid from all_college where id =" + str(i + 1))
            self.schoolid = self.cur.fetchone()[0]
            self.conn.commit()
            url = 'http://gkcx.eol.cn/schoolhtm/schoolSpecailtyMark/' + str(self.schoolid) + '/schoolSpecailtyMark.htm'
            self.getEachCourse_url(url)
            time.sleep(1)
            self.conn.commit()

        self.conn.close()
        print '结束'
        print '失效的链接有：'
        for i in self.wrong_url:
            print i


    def getEachCourse_url(self, url):
        try:
            print 'id= ', self.schoolid, '\n'
            selector = etree.HTML(self.session.get(url, headers=self.headers, timeout= 10).content)
            totalInfo = selector.xpath('//div[@class="S_result"]/table[@id="tableList"]/tr')
            for each_url in totalInfo:
                if each_url.xpath('td[1]/text()'):
                    province_name =  each_url.xpath('td[1]/text()')[0].replace('\r\n                           ', '')\
                        .replace('\r\n                     ', '')
                    for year in range(4):
                        if each_url.xpath('td[2]/a[' + str(year+1) +']/@href'):
                            li_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[2]/a[' + str(year+1) +']/@href')[0]
                            self.getData(li_url, province_name, self.schoolid)
                        if each_url.xpath('td[3]/a[' + str(year+1) +']/@href'):
                            wen_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[3]/a[' + str(year+1) +']/@href')[0]
                            self.getData(wen_url, province_name, self.schoolid)
                        if each_url.xpath('td[4]/a[' + str(year+1) +']/@href'):
                            zong_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[4]/a[' + str(year+1) +']/@href')[0]
                            self.getData(zong_url, province_name, self.schoolid)
                        if each_url.xpath('td[5]/a[' + str(year+1) +']/@href'):
                            yi_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[5]/a[' + str(year+1) +']/@href')[0]
                            self.getData(yi_url, province_name, self.schoolid)
                        if each_url.xpath('td[6]/a[' + str(year+1) +']/@href'):
                            ti_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[6]/a[' + str(year+1) +']/@href')[0]
                            self.getData(ti_url, province_name, self.schoolid)

        except:
            print '错误2, ', url


    def getData(self, url, name, schoolid):
        try:
            selector = etree.HTML(self.session.get(url, headers=self.headers, timeout= 10).content)
            info = selector.xpath('//div[@class="Scores"]/div[@class="S_result"]/table/tr')
            for each_info in info:
                if each_info.xpath('td[1]/text()'):
                    course_name = each_info.xpath('td[1]/text()')[0].replace(' ', '')
                else:
                    course_name = ''
                if each_info.xpath('td[2]/text()'):
                    year = each_info.xpath('td[2]/text()')[0]
                else:
                    year = ''
                if each_info.xpath('td[3]/text()'):
                    ave = each_info.xpath('td[3]/text()')[0]
                else:
                    ave = ''
                if each_info.xpath('td[4]/text()'):
                    max = each_info.xpath('td[4]/text()')[0]
                else:
                    max = ''
                if each_info.xpath('td[5]/text()'):
                    min = each_info.xpath('td[5]/text()')[0]
                else:
                    min = ''
                if each_info.xpath('td[6]/text()'):
                    s_type = each_info.xpath('td[6]/text()')[0].\
                        replace('                                                    \r\n                                                        ', '')\
                        .replace('\r\n                                                    ', '')
                else:
                    s_type = ''
                if each_info.xpath('td[7]/text()'):
                    admission_type = each_info.xpath('td[7]/text()')[0].\
                    replace('                                                    \r\n                                                        ', '').\
                    replace('\r\n                                                    ', '')
                else:
                    admission_type = ''
                #录入表中
                if year != '':
                    SQL = 'insert into course_line (schoolid,专业名称,年份,省份,平均分,最高分,最低分,考生类别,录取批次)' \
                          'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                          % (schoolid, course_name, year, name, ave, max, min, s_type, admission_type)
                    self.cur.execute(SQL)

        except:
            print '错误3, ', url
            self.wrong_url.append(url)
    def ex(self):
        r = self.session.get('http://gkcx.eol.cn/', headers=self.headers, timeout=10)
        cookies = r.cookies
        self.session.cookies.update(cookies)
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
        text = open('demo').read()
        ids = re.findall('specialty/(.*?)/', text, re.S)
        self.wrong_url = []
        for self.schoolid in ids:
            print '抓取',self.schoolid,'的数据'
            url = 'http://gkcx.eol.cn/schoolhtm/schoolSpecailtyMark/' + str(self.schoolid) + '/schoolSpecailtyMark.htm'
            self.getEachCourse_url(url)
            time.sleep(1)
            self.conn.commit()

        self.conn.close()
        print '结束'
        print '失效的链接有：'
        for i in self.wrong_url:
            print i


if __name__ == '__main__':
    c = course_line()
    # c.setupsession()
    c.ex()
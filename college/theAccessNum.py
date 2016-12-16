# -*-coding: utf8 -*-

'''
url =http://college.gaokao.com/school/tinfo(学校代码)/result/(省份代码)/(科目代码)/
一共 2666所大学
省份 1-31，香港 33，澳门38，台湾39
理科 1 ，文科 2，综合 3，其他 4，艺术理 8，艺术文 9
用遍历来完成对 url的创建
'''
import requests
import random
import MySQLdb
import time
from lxml import etree
import sys
reload(sys)


sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000000)


class theAccessNum():
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

        self.headers = {'Host': 'www.gaokao.com',
                        'User-Agent': random.choice(self.user_agent_list)
                        }
        self.session = requests.session()
        self.province = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                         24, 25, 26, 27, 28, 29, 30, 31, 33, 38, 39]
        self.type = [1, 2, 3, 4, 8, 9]
    def setupsession(self):
        try:
            r = self.session.get('http://www.gaokao.com', headers=self.headers)
            cookies = r.cookies
            self.session.cookies.update(cookies)
        except:
            print 'set up session 这里错误'

        #建立mysql链接
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
        self.urls = []
        return self.constructUrl()

    def constructUrl(self):
        for each_college in range(2666):
            for each_province in self.province:
                for each_type in self.type:
                    url = 'http://college.gaokao.com/school/tinfo'+ str(each_college) \
                          + '/result/' + str(each_province) + '/' + str(each_type) + '/'
                    self.getData(url)

        self.conn.close()
        print '未抓取的数据有'
        print self.urls
    def getData(self, url):
        try:
            #休眠0.1秒
            time.sleep(0.1)
            selector = etree.HTML(self.session.get(url, headers=self.headers).content)
            content = selector.xpath('//div[@id="wrapper"]/div[@class="cont_l in"]')
            '''
            将 学校+地区+考生类别 同 数据分开。遇到空数据，仍录入 学校+地区+考生类别的 数据.
            '''
            school_name = content.xpath('p[1]/font[1]/text()')[0]
            area = content.xpath('p[1]/font[2]/text()')[0]
            s_type = content.xpath('p[1]/font[3]/text()')[0]
            if content.xpath('div[@class="ts"]'):
            #无数据，返回空的插入
                SQL = 'insert into access_num(学校名称,地区,考生类别)values(\'%s\',\'%s\',\'%s\')'%(school_name, area, s_type)
                self.cur.execute(SQL)
                self.conn.commit()

            elif content.xpath('div[@id="pointbyarea"]/tr'):
            #有数据，采集
                for each_info in content.xpath('div[@id="pointbyarea"]/tr'):
                    if each_info.xpath('td[1]/text()'):
                        year = each_info.xpath('td[1]/text()')[0]
                    else: year = ''
                    if each_info.xpath('td[2]/text()'):
                        min = each_info.xpath('td[2]/text()')[0]
                    else: min = ''
                    if each_info.xpath('td[3]/text()'):
                        max = each_info.xpath('td[3]/text()')[0]
                    else: max = ''
                    if each_info.xpath('td[4]/text()'):
                        ave = each_info.xpath('td[4]/text()')[0]
                    else: ave = ''
                    if each_info.xpath('td[5]/text()'):
                        num = each_info.xpath('td[5]/text()')[0]
                    else: num = ''
                    if each_info.xpath('td[6]/text()'):
                        admission_type = each_info.xpath('td[6]/text()')[0]
                    else: admission_type = ''

                    if year != '':
                        SQL = 'insert into access_num(学校名称,地区,考生类别,年份,最低,最高,平均,录取人数,录取批次)' \
                          'value(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                          %(school_name, area, s_type, year, min, max, ave, num, admission_type)
                        self.cur.execute(SQL)
                        self.conn.commit()

        except:
            print '尝试重新连接, ',url
            self.urls.append(url)
if __name__ == '__main__':
    c =theAccessNum()
    c.setupsession()
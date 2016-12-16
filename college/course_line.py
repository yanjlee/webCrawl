# -*- coding:utf-8 -*-

import requests
import MySQLdb
import random
from lxml import etree
import sys
reload(sys)


sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000000)


class course_line():
    def __init__(self):
        self.user_agent_list = [ \
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
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
            r = self.session.get('http://gkcx.eol.cn/',headers=self.headers)
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
        return self.getUrl()

    def getUrl(self):
        for i in range(int(self.total_school)):
            self.cur.execute("select schoolid from all_college where id =" + str(i + 1))
            schoolid = self.cur.fetchone()[0]
            self.conn.commit()
            print '开始采集, id= ',schoolid,'\n'
            self.getEachCourse_url(schoolid)
        self.conn.close()
        print '未抓取的数据有'
        print self.urls

    def getEachCourse_url(self, schoolid):
        try:
            url = 'http://gkcx.eol.cn/schoolhtm/schoolSpecailtyMark/' + str(schoolid) + '/schoolSpecailtyMark.htm'
            selector = etree.HTML(self.session.get(url, headers=self.headers).content)
            totalInfo = selector.xpath('//div[@class="S_result"]/table[@id="tableList"]/tr')
            for each_url in totalInfo:
                if each_url.xpath('td[1]/text()'):
                    province_name =  each_url.xpath('td[1]/text()')[0].replace(' ','')
                # if name:
                #     province_name = name[0].replace(' ','')
                # print province_name
                # li_year_1 = each_url.xpath('td[2]/a[1]/@href')
                # if li_year_1:
                #     li_year_1_url = 'http://gkcx.eol.cn/' + li_year_1[0]
                #     self.getData(li_year_1_url, province_name, schoolid)
                # li_year_2 = each_url.xpath('td[2]/a[2]/@href')
                # if li_year_2:
                #     li_year_2_url = 'http://gkcx.eol.cn/' + li_year_2[0]
                #     self.getData(li_year_2_url, province_name, schoolid)
                # li_year_3 = each_url.xpath('td[2]/a[3]/@href')
                # if li_year_3:
                #     li_year_3_url = 'http://gkcx.eol.cn/' + li_year_3[0]
                #     self.getData(li_year_3_url, province_name, schoolid)
                # li_year_4 = each_url.xpath('td[2]/a[4]/@href')
                # if li_year_4:
                #     li_year_4_url = 'http://gkcx.eol.cn/' + li_year_4[0]
                #     self.getData(li_year_4_url, province_name, schoolid)
                # wen_year_1 = each_url.xpath('td[3]/a[1]/@href')
                # if wen_year_1:
                #     wen_year_1_url = 'http://gkcx.eol.cn/' + wen_year_1[0]
                #     self.getData(wen_year_1_url, province_name, schoolid)
                # wen_year_2 = each_url.xpath('td[3]/a[2]/@href')
                # if wen_year_2:
                #     wen_year_2_url = 'http://gkcx.eol.cn/' + wen_year_2[0]
                #     self.getData(wen_year_2_url, province_name, schoolid)
                # wen_year_3 = each_url.xpath('td[3]/a[3]/@href')
                # if wen_year_3:
                #     wen_year_3_url = 'http://gkcx.eol.cn/' + wen_year_3[0]
                #     self.getData(wen_year_3_url, province_name, schoolid)
                # wen_year_4 = each_url.xpath('td[3]/a[4]/@href')
                # if wen_year_4:
                #     wen_year_4_url = 'http://gkcx.eol.cn/' + wen_year_4[0]
                #     self.getData(wen_year_4_url, province_name, schoolid)
                # zong_year_1 = each_url.xpath('td[4]/a[1]/@href')
                # if zong_year_1:
                #     zong_year_1_url = 'http://gkcx.eol.cn/' + zong_year_1[0]
                #     self.getData(zong_year_1_url, province_name, schoolid)
                #     zong_year_2 = each_url.xpath('td[4]/a[2]/@href')
                # if zong_year_2:
                #     zong_year_2_url = 'http://gkcx.eol.cn/' + zong_year_2[0]
                #     self.getData(zong_year_2_url, province_name, schoolid)
                # zong_year_3 = each_url.xpath('td[4]/a[3]/@href')
                # if zong_year_3:
                #     zong_year_3_url = 'http://gkcx.eol.cn/' + zong_year_3[0]
                #     self.getData(zong_year_3_url, province_name, schoolid)
                # zong_year_4 = each_url.xpath('td[4]/a[4]/@href')
                # if zong_year_4:
                #     zong_year_4_url = 'http://gkcx.eol.cn/' + zong_year_4[0]
                #     self.getData(zong_year_4_url, province_name, schoolid)
                # 以上方法太慢
                    for year in range(4):
                        if each_url.xpath('td[2]/a[' + str(year+1) +']/@href'):
                            li_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[2]/a[' + str(year+1) +']/@href')[0]
                            self.getData(li_url, province_name, schoolid)
                        if each_url.xpath('td[3]/a[' + str(year+1) +']/@href'):
                            wen_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[3]/a[' + str(year+1) +']/@href')[0]
                            self.getData(wen_url, province_name, schoolid)
                        if each_url.xpath('td[4]/a[' + str(year+1) +']/@href'):
                            zong_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[4]/a[' + str(year+1) +']/@href')[0]
                            self.getData(zong_url, province_name, schoolid)
                        if each_url.xpath('td[5]/a[' + str(year+1) +']/@href'):
                            yi_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[5]/a[' + str(year+1) +']/@href')[0]
                            self.getData(yi_url, province_name, schoolid)
                        if each_url.xpath('td[6]/a[' + str(year+1) +']/@href'):
                            ti_url = 'http://gkcx.eol.cn/' + each_url.xpath('td[6]/a[' + str(year+1) +']/@href')[0]
                            self.getData(ti_url, province_name, schoolid)

        except:
            self.urls.append(url)

    def getData(self, url, name, schoolid):
        try:
            selector = etree.HTML(self.session.get(url, headers=self.headers).content)
            info = selector.xpath('//div[@class="Scores"]/div[@class="S_result"]/table/tr')
            for each_info in info:
                if each_info.xpath('td[1]/text()'):
                    course_name = each_info.xpath('td[1]/text()')[0].replace(' ','')
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
                    s_type = each_info.xpath('td[6]/text()')[0].replace(' ','')
                else:
                    s_type = ''
                if each_info.xpath('td[7]/text()'):
                    admission_type = each_info.xpath('td[7]/text()')[0].replace(' ','')
                else:
                    admission_type = ''
                #录入表中
                SQL = 'insert into course_line (schoolid,专业名称,年份,平均分,最高分,最低分,考生类别,录取批次)' \
                      'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                      %(schoolid, course_name, year, ave, max, min, s_type, admission_type)
                if course_name != '':
                    self.cur.execute(SQL)
                    self.conn.commit()
        except:
            self.urls.append(url)
if __name__ == '__main__':
    c = course_line()
    c.setupsession()

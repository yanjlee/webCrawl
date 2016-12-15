# -*-coding:utf-8-*-

import requests
import MySQLdb
import random
from lxml import etree
import sys
reload(sys)


sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000000)


class admissionLine():
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
        r = self.session.get('http://gkcx.eol.cn/',headers=self.headers)
        cookies = r.cookies
        self.session.cookies.update(cookies)
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
        return self.getUrl()

    def getUrl(self):
        for i in range(int(self.total_school)):
            self.cur.execute("select schoolid from all_college where id =" + str(i + 1))
            schoolid = self.cur.fetchone()[0]
            self.conn.commit()
            print '开始采集, id= ',schoolid
            self.getEachProvince_url(schoolid)

        self.conn.close()
    def getEachProvince_url(self,schoolid):
        url = 'http://gkcx.eol.cn/schoolhtm/schoolAreaPoint/' + str(schoolid) + '/schoolAreaPoint.htm'
        selector = etree.HTML(self.session.get(url, headers=self.headers).content)
        province = selector.xpath('//div[@class="S_result"]/table[@id="tableList"]/tr')
        print 'id= ',schoolid,'的url'
        for each_url in province:
            name = each_url.xpath('td[1]/text()')
            if name:
                province_name = name[0]
            wen_line = each_url.xpath('td[2]/a/@href')
            if wen_line:
                wen_url = 'http://gkcx.eol.cn/' + wen_line[0]
                self.getData(wen_url, province_name, schoolid)
            li_line = each_url.xpath('td[3]/a/@href')
            if wen_line:
                li_url = 'http://gkcx.eol.cn/' + li_line[0]
                self.getData(li_url, province_name, schoolid)
            zong_line = each_url.xpath('td[4]/a/@href')
            if wen_line:
                zong_url = 'http://gkcx.eol.cn/' + li_line[0]
                self.getData(zong_url, province_name, schoolid)
            yi_line = each_url.xpath('td[5]/a/@href')
            if yi_line:
                yi_url = 'http://gkcx.eol.cn/' + li_line[0]
                self.getData(yi_url, province_name, schoolid)
            ti_line = each_url.xpath('td[6]/a/@href')
            if ti_line:
                ti_url = 'http://gkcx.eol.cn/' + li_line[0]
                self.getData(ti_url, province_name, schoolid)


    def getData(self, url, name, schoolid):
        selector = etree.HTML(self.session.get(url, headers=self.headers).content)
        info = selector.xpath('//div[@class="Scores"]/div[@class="S_result"]/table/tr')
        for each_info in info:
            year = each_info.xpath('td[1]/text()')
            if year:
                year = year[0]
            else :
                year = ''

            max = each_info.xpath('td[2]/text()')
            if max:
                max = max[0]
            else:
                max = ''

            ave = each_info.xpath('td[3]/text()')
            if ave:
                ave = ave[0]
            else:
                ave = ''

            line = each_info.xpath('td[4]/text()')
            if line:
                line = line[0]
            else:
                line = ''

            s_type = each_info.xpath('td[5]/text()')
            if s_type:
                s_type = s_type[0]
            else:
                s_type = ''

            admission_type = each_info.xpath('td[6]/text()')
            if admission_type:
                admission_type = admission_type[0]
            else:
                admission_type = ''

            #然后录入表中
            if year != '':
                SQL = 'insert into admission_line(schoolid,年份,省份,最高分,平均分,省控线,考生类别,录取批次)values' \
                  '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                  %(schoolid, year, name, max, ave, line, s_type, admission_type)
                self.cur.execute(SQL)
                self.conn.commit()

if __name__ == '__main__':
    c = admissionLine()
    c.setupsession()
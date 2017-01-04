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
        self.sname = []
        self.urls = []

    def setupsession(self):
        sql_total = 'select count(*) from new_全国高校基本数据'
        self.cur.execute(sql_total)
        result = self.cur.fetchone()[0]
        for i in range(2624, result):
            #获取大学的url地址
            sql_url = 'select 院校名称,url from new_全国高校基本数据 where id = \'' + str(i+1) + '\''
            self.cur.execute(sql_url)
            result2 = self.cur.fetchone()
            if result2:
                schoolname = result2[0]
                url = result2[1]
                #转跳抓取网页
                print i
                self.constructUrl(url, schoolname)
                time.sleep(2)

        #结束时候返回错误
        self.ex()

    def constructUrl(self, url, schoolname):
        if len(self.sname) is not 0:
            self.ex()
        else:
            newUrl = url + 'fee/'
            print '录入', schoolname,'\n'
            headers = {'Host': 'college.zjut.cc'}
            selector = etree.HTML(self.session.get(newUrl, headers=headers).content)
            return self.getData(selector, schoolname, newUrl)

    def getData(self, selector, schoolname, url):
        try:
            if selector.xpath('//div[@id="fee1"]'):
                if selector.xpath('//div[@id="fee1"]/div[@class="table-responsive"]/table/tbody/tr'):
                    content = selector.xpath('//div[@id="fee1"]/div[@class="table-responsive"]/table/tbody/tr')
                    for each in content:
                        if each.xpath('td[4]/p/text()')[0] == '学费标准':
                            continue
                        else:
                            name = each.xpath('td[3]/p/text()')[0]
                            fee = each.xpath('td[4]/p/text()')[0]
                            sql2 = 'insert into new_各校各专业学费(学校名称,专业名称,学费)values' \
                                   '(\'%s\',\'%s\',\'%s\')' % (schoolname, name, fee)
                            print sql2
                    #         self.cur.execute(sql2)
                    # self.conn.commit()
                else:
                    content1 = selector.xpath('//div[@id="fee1"]')[0]
                    content1_2 = content1.xpath('string(.)')
                    sql1 = 'insert into new_各校各专业学费(学校名称,额外)values(\'%s\',\'%s\')'% (schoolname, content1_2)
                    print sql1
                    # self.cur.execute(sql1)
            else:
                content1_2 = ''

            if selector.xpath('//div[@class="table-responsive"]'):
                content = selector.xpath('//div[@class="table-responsive"]/table/tbody/tr')
                for each in content:
                    if each.xpath('td[1]/text()'):
                        name = each.xpath('td[1]/text()')[0]
                        fee = each.xpath('td[2]/text()')[0]
                        beizhu = each.xpath('td[3]/text()')[0]
                        sql3 = 'insert into new_各校各专业学费(学校名称,专业名称,学费,备注)values' \
                                '(\'%s\',\'%s\',\'%s\',\'%s\')' % (schoolname, name, fee, beizhu)
                        print sql3
                #         self.cur.execute(sql3)
                # self.conn.commit()
        except:
            print '录入错误',schoolname, url
            self.sname.append(schoolname)
            self.urls.append(url)

    def ex(self):
        if self.sname:
            for i in range(len(self.sname)):
                print '补充录入,第',i,'个'
                self.constructUrl(self.urls[i], self.sname[i])
            self.sname = []
            self.urls = []

            return self.constructUrl()
        else:
            print '录入结束'
            self.conn.close()



if __name__ == '__main__':
    f = feeOfEachCollege()
    f.setupsession()

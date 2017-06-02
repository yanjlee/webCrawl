# -*- coding:utf8 -*-

import requests
import random
import MySQLdb
from lxml import etree

class Academy():
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
        self.session = requests.session()

    def setupsession(self):
        try:
            headers = {
                'Host': 'www.gaokao.com',
                'User-Agent': random.choice(self.user_agent_list),
            }
            r = self.session.get('http://www.gaokao.com', headers=headers)
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
            self.urls = []
            return self.constructUrl()
        except:
            print 'set up session 这里错误'

    def constructUrl(self):
        for i in range(1):
            url = 'http://college.gaokao.com/school/tinfo/' + str(i+1) + '/yuanxi/'
            self.withChoice(url)
        print '抓取完毕'
        self.conn.close()
        print '失效的链接有'
        for wrong_link in self.urls:
            print wrong_link
    def withChoice(self, url):
        '''
        院系有三种表达结构，一种是没有，一种是列表，一种是表格
        '''
        headers = {
            'Host': 'college.gaokao.com',
            'User-Agent': random.choice(self.user_agent_list),
        }
        selector = etree.HTML(self.session.get(url, headers=headers).content)
        school_name = selector.xpath('//div[@class="wrap"]/div[@class="bg_sez"]/h2/text()')[0]
        if selector.xpath('//div[@class="jj"]/table/tr'):
            for each_info in selector.xpath('//div[@class="jj"]/table/tr'):
                #获取院系名称
                ac_name = each_info.xpath('td[1]/p/text()')[0].replace(' ','')
                if each_info.xpath('td[2]'):
                    if each_info.xpath('td[2]/p/text()'):
                        c_name = each_info.xpath('td[2]/p/text()')[0].replace(' ','')
                        if ac_name != '学院':
                            SQL = 'insert into academy (大学名称,院系名称,专业名称)values' \
                                '(\'%s\',\'%s\',\'%s\')'%(school_name, ac_name, c_name)
                            self.cur.execute(SQL)
                            self.conn.commit()
                    else:
                        if ac_name != '学院':
                            SQL = 'insert into academy(大学名称,院系名称)values(\'%s\',\'%s\')' % (school_name, ac_name)
                            self.cur.execute(SQL)
                            self.conn.commit()
                else:
                    SQL = 'insert into academy(大学名称,院系名称)values(\'%s\',\'%s\')'%(school_name, ac_name)
                    self.cur.execute(SQL)
                    self.conn.commit()
        elif selector.xpath(''):
            pass
        #在获取院系信息，不同院校的表达不同。比较难


if __name__ == '__main__':
    c = Academy()
    c.setupsession()
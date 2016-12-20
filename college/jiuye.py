# -*- coding:utf8 -*-

'''
爬去学信网上的专业就业情况(http://gaokao.chsi.com.cn/z/jylfb/),看似数据很好抓取，获取页面中每个专业在标签里的专业id，通过
'http://gaokao.chsi.com.cn/sch/jy/query.do?method=showJyxxById'用post获取专业的就业情况和毕业生规模。
一开始陷入误区就是，在获取专业id时，编写爬虫脚本，发现是嵌套形式的，然后获取表格，想如何爬取表格，这时候发现用xpath爬取的数据是乱码，也就是网页有反
爬策略，此时想到正则表达式，把网页html保存下来，用regex来获取各专业id，然后再去获取详细情况，关于文字内容是乱码，在爬取详细情况时候得到确认
'''
import requests
from lxml import etree
import time
import re
import MySQLdb
import sys
import random


reload(sys)
sys.setdefaultencoding('utf8')


class jiuyeqingkuang():
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
        headers = {
            'User-Agent': random.choice(self.user_agent_list),
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://gaokao.chsi.com.cn/z/jylfb/',
            'Origin': 'http://gaokao.chsi.com.cn',
            'Host': 'gaokao.chsi.com.cn'
        }
        self.session = requests.session()
        self.session.headers.update(headers)
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()

    def getAllIds(self):
        # category = re.findall('color:#376F00;">(.*?)</td>', html_benke, re.S)
        # print category[1]
        # for i in category:
        #     print i.replace('\n\t\t\t\t','').replace('\n\t\t\t','')
        html_benke = open('benke').read()
        html_zhuanke = open('zhuanke').read()
        course = re.findall('getSpecialities(.*?);return false;', html_benke, re.S)
        for p in course:
            id = re.search('\'(.*?)\'', p, re.S).group(1)
            name = re.search(',\'(.*?)\'\)', p, re.S).group(1)
            self.getData_ben(id, name)
            time.sleep(1)

        course_zhuan = re.findall('getSpecialities(.*?);return false;', html_zhuanke, re.S)
        for p in course_zhuan:
            id = re.search('\'(.*?)\'', p, re.S).group(1)
            name = re.search(',\'(.*?)\'\)', p, re.S).group(1)
            self.getData_zhuan(id, name)
            time.sleep(1)

        print '抓取完毕'
        self.conn.close()


    def getData_ben(self, id, name):
        url = 'http://gaokao.chsi.com.cn/sch/jy/query.do?method=showJyxxById'
        data = {'id': id}
        type = '本科'
        selector = etree.HTML(self.session.post(url, data=data).content)
        sid = selector.xpath('//table/tr[1]/td[2]/text()')[0]
        rate = selector.xpath('//table/tr[3]/td[2]/text()')[0]
        num = selector.xpath('//table/tr[4]/td[2]/text()')[0]
        SQL = 'insert into jiuyeqingkuang(层次,专业代码,专业名称,就业率区间,毕业生规模)' \
              'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(type, sid, name, rate, num)
        self.cur.execute(SQL)
        self.conn.commit()

    def getData_zhuan(self, id, name):
        url = 'http://gaokao.chsi.com.cn/sch/jy/query.do?method=showJyxxById'
        data = {'id': id}
        type = '专科'
        selector = etree.HTML(self.session.post(url, data=data).content)
        sid = selector.xpath('//table/tr[1]/td[2]/text()')[0]
        rate = selector.xpath('//table/tr[3]/td[2]/text()')[0]
        num = selector.xpath('//table/tr[4]/td[2]/text()')[0]
        SQL = 'insert into jiuyeqingkuang(层次,专业代码,专业名称,就业率区间,毕业生规模)' \
              'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(type, sid, name, rate, num)
        self.cur.execute(SQL)
        self.conn.commit()

if __name__ == '__main__':
    c = jiuyeqingkuang()
    c.getAllIds()
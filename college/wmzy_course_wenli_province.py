# -*-coding:utf8-*-

'''
抓取各大学在各省的招生专业
def __init__(self) 这个初始化函数可以扔到后面
'''

import requests
import random
import MySQLdb
import re
from lxml import etree
import sys
reload(sys)
sys.setrecursionlimit(2000000)

sys.setdefaultencoding('utf-8')

class getEachProvince_wenliInfo():
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
                        'Host': 'www.wmzy.com'}
        self.cookies = {
            'Cookie': 'guide=1;'
                      ' sessionid=s:EsEpQkmCHUXEct7jVHKXwLyK.fm+4BeS95NUVpu9+8nr1nrrgLb+jWt6PbEp1UHLeErk;'
                      ' _gat=1;'
                      ' Hm_lvt_02ceb62d85182f1a72db7d703affef9c=1485224333,1485274811,1486178337,1486257750;'
                      ' Hm_lpvt_02ceb62d85182f1a72db7d703affef9c=1486257782;'
                      ' _ga=GA1.2.41898681.1485053816;'
                      ' Hm_lvt_8a2f2a00c5aff9efb919ee7af23b5366=1485224333,1485274811,1486178338,1486257750;'
                      ' Hm_lpvt_8a2f2a00c5aff9efb919ee7af23b5366=1486257858'
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)

        # 创建mysql链接
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='wmzy_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        self.cur.execute('set sql_safe_updates=0;')

    def setupsession(self):
        province = {33: '浙江', 53: '云南', 65: '新疆', 54: '西藏', 12: '天津', 31: '上海', 51: '四川', 61: '陕西',
                    37: '山东', 14: '山西', 63: '青海', 15: '内蒙古', 64: '宁夏', 21: '辽宁', 32: '江苏', 36: '江西',
                    22: '吉林', 13: '河北', 41: '河南', 43: '湖南', 23: '黑龙江', 46: '海南', 42: '湖北', 45: '广西',
                    44: '广东', 52: '贵州', 62: '甘肃', 35: '福建', 50: '重庆', 11: '北京', 34: '安徽'}
        year = [2012, 2013, 2014]
        wenli = {'wenscore': '文史', 'liscore': '理工'}
        self.cur.execute('set sql_safe_updates=0')
        self.cur.execute('select * from college_info where id>=102')
        list = self.cur.fetchall()
        for each in list:
            scname = each[1]
            sctype = each[3]
            url = 'http://www.wmzy.com/api/school-rank/' + each[7].replace('http://www.wmzy.com/api/school/', '')
            for p in province.keys():
                for t in wenli.keys():
                    for y in year:
                        params = {
                            'rankingType': t,
                            'year': y,
                            'province': p
                        }
                        print scname, sctype, province[p], t, y
                        self.get_urls(self.session.get(url, params=params).
                                    content, scname, sctype, province[p], wenli[t], y)


    def get_urls(self, content, cname, ctype, p, wenli, y):
        selector = etree.HTML(content)
        if selector.xpath('//table[@class="ranking-table"]'):
            if selector.xpath('//table[@class="ranking-table"]/tbody/tr/th'):
                # 此页没有数据
                pass
            else:
                self.get_data(content, cname, ctype, p, wenli, y)
                for each in selector.xpath('//div[@class="page"]/a'):
                    if each.xpath('text()'):
                        if each.xpath('@href'):
                            each_url = 'http://www.wmzy.com' + each.xpath('@href')[0]
                            self.get_data(self.session.get(each_url).content, cname, ctype, p, wenli, y)


    def get_data(self, content, cname, ctype, p, wenli, y):
        selector = etree.HTML(content)
        for each in selector.xpath('//table[@class="ranking-table"]/tbody/tr'):
            rank = each.xpath('td[1]/text()')[0]
            name = each.xpath('td[2]/a/text()')[0]
            ex_info = each.xpath('td[2]/div')[0].xpath('string(.)').replace(' ', '').replace('\n', '')
            in_1 = each.xpath('td[3]/text()')[0]
            in_2 = each.xpath('td[4]/text()')[0]
            # print rank, name, ex_info, in_1, in_2
            sql = 'insert into college_eachProvince_wenli' \
                  '(院校名称,本专科,省份,年份,文理科,排名,专业名称,专业信息,招生规模,录取平均分)values' \
                  '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                  % (cname, ctype, p, y, wenli, rank, name, ex_info, in_1, in_2)
            self.cur.execute(sql)
        self.conn.commit()
if __name__ == '__main__':
    c = getEachProvince_wenliInfo()
    c.setupsession()
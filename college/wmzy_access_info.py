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

class eachCollege_accessInfo():
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
        self.province = {340000000000: '安徽', 110000000000: '北京', 500000000000: '重庆', 350000000000: '福建',
                    620000000000: '甘肃', 440000000000: '广东', 450000000000: '广西', 520000000000: '贵州',
                    460000000000: '海南', 130000000000: '河北', 410000000000: '河南', 230000000000: '黑龙江',
                    420000000000: '湖北', 430000000000: '湖南', 220000000000: '吉林', 320000000000: '江苏',
                    360000000000: '江西', 210000000000: '辽宁', 150000000000: '内蒙古',640000000000: '宁夏',
                    630000000000: '青海', 370000000000: '山东', 140000000000: '山西', 610000000000: '陕西',
                    310000000000: '上海', 510000000000: '四川', 120000000000: '天津', 650000000000: '新疆',
                    530000000000: '云南', 330000000000: '浙江'}
        self.year = [2015, 2014, 2013, 2012]
        self.wenli = {'li': '理工', 'wen': '文史'}
    def setupsession(self):
        self.cur.execute('set sql_safe_updates=0')
        self.cur.execute('select * from college_info')
        list = self.cur.fetchall()
        n = 1
        for each in list:
            scname = each[1]
            sctype = each[3]
            url = 'http://www.wmzy.com/api/school-score/' + each[7].replace('http://www.wmzy.com/api/school/', '')
            print n, scname, sctype
            n += 1
            for p in self.province.keys():
                for t in self.wenli:
                    self.get_data_1(self.session.get(url).content, p, t, scname, sctype)
                    for y in self.year:
                        params = {
                            'year': y,
                            'province': p,
                            'ty': t
                        }
                        self.get_data_2(self.session.get(url, params=params).content, p, y, t, scname, sctype)
        self.conn.close()
    def get_data_1(self, content, p, t, scname, sctype):
        selector = etree.HTML(content)
        if selector.xpath('//table[1]/tbody/tr'):
            for each in selector.xpath('//table[1]/tbody/tr'):
                info = {}
                for i in range(7):
                    if each.xpath('td[' + str(i+1) + ']/text()'):
                        info[i] = each.xpath('td[' + str(i+1) + ']/text()')[0]
                    else:
                        info[i] = ''
                sql_1 = 'insert into each_college_line(院校名称,本专科,省份,年份,最高分,平均分,' \
                        '平均分线差,最低分,录取人数,批次,文理科)values' \
                        '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                        % (scname, sctype, self.province[p], info[0], info[1], info[2], info[3],
                           info[4], info[5], info[6], self.wenli[t])
                self.cur.execute(sql_1)
            self.conn.commit()
    def get_data_2(self, content, p, y, t, scname, sctype):
        text = re.findall('majorsData":(.*)', re.findall('PageData(.*?)catch', content, re.S)[0], re.S)[0]
        if re.findall('major_index(.*?)}', text, re.S):
            for each in re.findall('major_index(.*?)}', text, re.S):
                # print each
                pici = re.findall('major_batch":"(.*?)","major', each, re.S)[0]
                zhuanye = re.findall('major_name":"(.*?)","major_', each, re.S)[0]
                fenshu = re.findall('major_score":(.*?),"majo', each, re.S)[0]
                weici = re.findall('major_score_rank":(.*)', each, re.S)[0]
                num = re.findall('major_total_count":(.*?),"major', each, re.S)[0]
                sql = 'insert into each_college_mingci(院校名称,本专科,文理科,专业名称,录取分数,对应位次,本次录取人数,省份,年份)' \
                      'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                      % (scname, sctype, self.wenli[t], zhuanye, fenshu, weici, num, self.province[p], y)
                self.cur.execute(sql)
            self.conn.commit()
if __name__ == '__main__':
    c = eachCollege_accessInfo()
    c.setupsession()
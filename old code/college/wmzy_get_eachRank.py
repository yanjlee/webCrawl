# -*-coding:utf8-*-
'''
抓取各类榜单,知名度,竞争力,薪酬,妹纸
'''
import requests
import time
import random
import MySQLdb
import re
from lxml import etree
import sys
reload(sys)
sys.setrecursionlimit(2000000)

sys.setdefaultencoding('utf-8')

class getEachRank():
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
        # 论证页面是否为空
        self.K = False
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

    def setupsession(self):
        url = 'http://www.wmzy.com/api/rank/school'
        n = 1
        while(True):
            params_zhimingdu = {
                'diploma': 7,
                'rankType': 'zhimingdu',
                'province': '',
                'searchKey': '',
                'page': n,
                'count': 100,
                'diploma_id': 7,
                '_': 1486347773032
            }
            params_jingzhengli = {
                'diploma': 7,
                'rankType': 'jingzhengli',
                'province': '',
                'searchKey': '',
                'page': n,
                'count': 100,
                'diploma_id': 7,
                '_': 1486347796168
            }
            params_xinchou = {
                'diploma': 7,
                'rankType': 'xinchou',
                'province': '',
                'searchKey': '',
                'page': n,
                'count': 100,
                'diploma_id': 7,
                '_': 1486348081156
            }
            params_meizhi = {
                'diploma': 7,
                'rankType': 'meizhi',
                'province': '',
                'searchKey': '',
                'page': n,
                'count': 100,
                'diploma_id': 7,
                '_': 1486348174219
            }
            params_xinchou_z = {
                'diploma': 5,
                'rankType': 'xinchou',
                'province': '',
                'searchKey': '',
                'page': n,
                'count': 100,
                'diploma_id': 7,
                '_': 1486353375132
            }
            params_meizhi_z = {
                'diploma': 5,
                'rankType': 'meizhi',
                'province': '',
                'searchKey': '',
                'page': n,
                'count': 100,
                'diploma_id': 7,
                '_': 1486353401883
            }
            # self.do_clear(self.session.get(url, params=params_jingzhengli).content)
            # self.do_clear(self.session.get(url, params=params_zhimingdu).content)
            # self.do_clear(self.session.get(url, params=params_xinchou).content)
            # self.do_clear(self.session.get(url, params=params_meizhi).content)
            # 以下都是专科
            # self.do_clear(self.session.get(url, params=params_xinchou_z).content)
            self.do_clear(self.session.get(url, params=params_meizhi_z).content)

            if self.K:
                n += 1
                continue
            elif self.K is False:
                break

    def do_clear(self, content):
        '''
        这里作为本科数据清洗,提取出需要的信息
        :param content:
        :return: 如果信息为空，返回，并break
        '''
        text_totle = re.findall('table(.*?)table>', content.replace(' ', ''), re.S)[0]
        text_title = re.findall('thead(.*?)thead>', text_totle, re.S)[0]
        t1 = re.findall('col1(.*?)<', text_title, re.S)[0].replace('\\">', '')
        t2 = re.findall('col2(.*?)<', text_title, re.S)[0].replace('\\">', '')
        t3 = re.findall('col3(.*?)<', text_title, re.S)[0].replace('\\">', '')
        t4 = re.findall('col4(.*?)<', text_title, re.S)[0].replace('\\">', '')
        t5 = re.findall('col5(.*?)<', text_title, re.S)[0].replace('\\">', '')
        if re.findall('\<tdclass=(.*?)\</tr\>', text_totle, re.S):
            self.K = True
            list = re.findall('\<tdclass=(.*?)\</tr\>', text_totle, re.S)
            for each in list:
                # print each
                #本科专科是分别两个regex来导出的
                sc_name_z =re.findall('diploma=5(.*?)a', each, re.S)[0].replace('\\">', '').replace('</', '')
                # sc_name = re.findall('html(.*?)a', each, re.S)[0].replace('\\">', '').replace('</', '')
                type = re.findall('<td>(.*?)</td>', each, re.S)[0]
                location = re.findall('<td>(.*?)\</td>', each, re.S)[1]
                provide_type = re.findall('<td>(.*?)</td>', each, re.S)[2].replace('/', '及')
                s = re.findall('<td>(.*?)\</td>', each, re.S)[3].replace('￥', '')
                url = 'http://www.wmzy.com' \
                      + re.findall('href=(.*?)"\>', each, re.S)[0].replace('\\"', '').replace('\\', '')
                # print sc_name, type, location, provide_type, s
                # sql = 'insert into college_rank(%s,%s,%s,%s,%s,url,本专科)' \
                #       'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                #       % (t1, t2, t3, t4, t5, sc_name, type, location, provide_type, s, url, '本科')
                # self.cur.execute(sql)
                sql_z = 'insert into college_rank(%s,%s,%s,%s,%s,url,本专科)' \
                      'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                      % (t1, t2, t3, t4, t5, sc_name_z, type, location, provide_type, s, url, '专科')

                self.cur.execute(sql_z)
                self.conn.commit()

        else:
            self.K = False


if __name__ == '__main__':
    c = getEachRank()
    c.setupsession()
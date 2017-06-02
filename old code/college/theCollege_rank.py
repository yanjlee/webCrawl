# -*-coding:utf-8 -*-

import requests
import MySQLdb
import sys
import json
import time
import random


reload(sys)
sys.setdefaultencoding('utf8')


class rank():
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
        header = {
        'User-Agent': random.choice(self.user_agent_list),
        'Host': 'www.gaokaopai.com',
        'Origin': 'http://www.gaokaopai.com',
        'X-Requested-With': 'XMLHttpRequest'
        }
        cookies = {
            'Cookie': 'aliyungf_tc=AQAAAH9BZBCrFw8A5RuWtvV9sWllzSFb;'
                      ' acw_tc=AQAAAL2Y8xOkLA8A5RuWttSQe5pUa3S/;'
                      ' PHPSESSID=brtc942pnklsph78j7difqhsf2;'
                      ' firstEnterUrlInSession=http%3A//www.gaokaopai.com/;'
                      ' VisitorCapacity=1;'
                      ' acw_sc=585b95332885509c7d1d10caa0ff4300f7eabf18;'
                      ' Hm_lvt_c2c1aeb9dd53d590e8d4109d912eed04=1482376087;'
                      ' Hm_lpvt_c2c1aeb9dd53d590e8d4109d912eed04=1482398089'
        }
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        self.session = requests.session()
        self.session.headers.update(header)
        self.session.cookies.update(cookies)
    def setupsession(self):
        url = 'http://www.gaokaopai.com/rank-index.html'
        # self.wulianshu(url)
        self.nandu(url)
        self.conn.close()
    def nandu(self, url):
        for i in range(1,7):
            data = {
                'otype': 4,
                'city': '',
                'start': i*25,
                'amount': 25
            }
            header = {'Referer': 'http://www.gaokaopai.com/paihang-otype-4.html'}
            r = self.session.post(url, data=data, headers=header)
            print r.status_code
            print r.content
            time.sleep(1)
            jsDict = json.loads(r.content)['data']
            jsContent = jsDict['ranks']
            for info in jsContent:
                rank = info['rank']
                name = info['uni_name']
                safe_h = info['safehard']
                area = info['city_code']
                type = info['uni_type']
                SQL = 'insert into  college_rank_nandu(排名,院校名称,录取难度,院校所在地,类型)values' \
                  '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' %(rank, name, safe_h, area, type)
                self.cur.execute(SQL)
                self.conn.commit()
        time.sleep(1)
        print 'over'


    def wulianshu(self, url):
        for i in range(1,7):
            data = {
                'otype': 3,
                'city': 'undefined',
                'cate': 'undefined',
                'batch_type': 'undefined',
                'start': i*25,
                'amount': 25
            }
            header = {'Referer': 'http://www.gaokaopai.com/paihang-otype-3.html'}
            r = self.session.post(url, data=data, headers=header)
            jsDict = json.loads(r.content)['data']
            jsContent = jsDict['ranks']
            for info in jsContent:
                rank = info['category_3']
                name = info['uni_name']
                area = info['city_code']
                type = info['uni_type']
                total = info['wu_total']
                train = info['wu_training_score']
                science = info['wu_scientific_score']
                SQL = 'insert into college_rank_wulianshu(排名,院校名称,总分,人才培养,科学培养,类型,所在地)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(rank, name, total, train, science, type, area)
                self.cur.execute(SQL)
                self.conn.commit()
        print '录入完毕'


if __name__ == '__main__':
    c = rank()
    c.setupsession()
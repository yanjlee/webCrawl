# -*-coding:utf8 -*-

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


class getEachCollegeScheNum():
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
                        'Host': 'www.zjut.cc'}
        self.session = requests.session()
        r = self.session.get('http://www.zjut.cc/zs_10001/fenshuxian.html')
        self.session.headers.update(self.headers)
        self.session.cookies.update(r.cookies)
        self.formhash = re.findall('formhash: "(.*?)",', r.content, re.S)[0]
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        # self.province = [11, 13, 14, 21, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 50, 52, 53, 61, 62, 63,
        #                  51, 22, 15, 64, 65, 58, 12]
        self.provinces = {11: '北京', 12: '天津', 13: '河北省', 14: '山西省', 15: '内蒙古', 21: '辽宁省', 22: '吉林省',
                          23: '黑龙江省', 31: '上海', 32: '江苏省', 33: '浙江省', 34: '安徽省', 35: '福建省', 36: '江西省',
                          37: '山东省', 41: '河南省', 42: '湖北省', 43: '湖南省', 44: '广东省', 45: '广西省', 46: '海南省',
                          50: '重庆', 51: '四川省', 52: '贵州省', 53: '云南省', 61: '陕西省', 62: '甘肃省', 63: '青海省',
                          64: '宁夏', 65: '新疆', 58:'西藏'}
        self.year = [2014, 2015, 2016]
    def doSearchAllCollege(self):
        sql_total = 'select count(*) from new_全国高校基本数据'
        self.cur.execute(sql_total)
        result = self.cur.fetchone()[0]
        for i in range(result):
            # 获取大学的url地址
            sql_url = 'select 院校名称,url from new_全国高校基本数据 where id = \'' + str(i + 1) + '\''
            self.cur.execute(sql_url)
            result2 = self.cur.fetchone()
            if result2:
                schoolname = result2[0]
                url = result2[1]
                # 转跳抓取网页
                print '第', i + 1, '所', schoolname
                self.construction(url, schoolname)
                # time.sleep(1)
        # 抓取结束，关闭链接
        self.conn.close()

    def construction(self, url, schoolname):
        sc_id = url.replace('http://college.zjut.cc/', '').replace('/', '')
        do_url = 'http://www.zjut.cc/zs.php'
        for no in self.provinces.keys():
            for y in self.year:
                data = {
                    'mod': 'api',
                    'ac': 'plan',
                    'formhash': self.formhash,
                    'id': sc_id,
                    'ssdm': no,
                    'year': y,
                    'plansubmit': 'true'
                    }
                self.getData(self.session.post(do_url, data=data).content, no, y, schoolname)
            # time.sleep(1)
        # 在一个学校抓完31省数据后再commit
        self.conn.commit()
    def getData(self, content, no, y, schoolname):
        print self.provinces[no], y
        selector = etree.HTML(content.decode('utf8'))
        if selector.xpath('//table/tbody/tr'):
            course_name = selector.xpath('//table[@class="table table-hover"]/thead/tr/th[1]/text()')[0]
            type = selector.xpath('//table[@class="table table-hover"]/thead/tr/th[2]/text()')[0]
            cengci = selector.xpath('//table[@class="table table-hover"]/thead/tr/th[3]/text()')[0]
            kelei = selector.xpath('//table[@class="table table-hover"]/thead/tr/th[4]/text()')[0]
            jihuashu = selector.xpath('//table[@class="table table-hover"]/thead/tr/th[5]/text()')[0]
            content = selector.xpath('//table/tbody/tr')
            for each in content:
                c_n = each.xpath('td[1]')[0].xpath('string(.)').replace("'", '')
                c_type = each.xpath('td[2]/text()')[0]
                c_cengci = each.xpath('td[3]/text()')[0]
                c_kelei = each.xpath('td[4]/text()')[0]
                c_jihua = each.xpath('td[5]/text()')[0]
                sql = 'insert into new_各校历年各省招生计划(%s,%s,%s,%s,%s,%s,%s,%s)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % ('院校名称', '省份', '年份', \
                course_name, type, cengci, kelei, jihuashu, schoolname, self.provinces[no], y, c_n, c_type, c_cengci,
                 c_kelei, c_jihua)
                self.cur.execute(sql)


if __name__ == '__main__':
    f = getEachCollegeScheNum()
    f.doSearchAllCollege()
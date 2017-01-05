# -*-coding:utf8 -*-
'''
这几天一直在对服务器做压力测试，挺稳定的，就没有用try/except
一共31个省，但数据只有24个省的
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


class getEachCollegeAccessNum():
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
        self.province = [11, 13, 14, 21, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 50, 52, 53, 61, 62, 63,
                         51, 22, 15, 64, 65, 58, 12]
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
                print '第', i+1, '所', schoolname
                self.construction(url, schoolname)
            time.sleep(1)
        #抓取结束，关闭链接
        self.conn.close()
    def construction(self, url, schoolname):
        sc_id = url.replace('http://college.zjut.cc/', '').replace('/', '')
        do_url = 'http://www.zjut.cc/zs.php'
        for no in self.province:
            data = {
                'mod': 'api',
                'ac': 'xkx',
                'formhash': self.formhash,
                'id': sc_id,
                'ssdm': no,
                'xkxsubmit': 'true'
            }
            self.getData(self.session.post(do_url, data=data).content, no, schoolname)
            time.sleep(1)

        #在一个学校抓完31省数据后再commit
        self.conn.commit()

    def getData(self, content, no, schoolname):
        if content is not '':
            if no is 11:
                no = '北京'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidifen = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    yuwen = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    shuxue = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    waiyu = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    zonghe = selector.xpath('//table/thead/tr/th[9]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(9):
                            if each.xpath('td[' + str(i+1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i+1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
                              % ('院校名称', '省份', year, type, pici, beizhu, zuidifen, yuwen, shuxue, waiyu, zonghe,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'])
                        self.cur.execute(sql)
                        d = {}
            if no is 13:
                no = '河北省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    yuwen = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    shuxue = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    waiyu = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(8):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, '投档最低分含优惠', yuwen, shuxue, waiyu,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'])
                        self.cur.execute(sql)
                        d = {}

            if no is 14:
                no = '山西省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    xingzhi = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    zuidifen = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(6):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''

                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s)values' \
                                '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                                % ('院校名称', '省份', year, type, pici, xingzhi, beizhu, zuidifen,
                                    schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'])
                        self.cur.execute(sql)
                        d = {}
            if no is 21:
                no = '辽宁省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidifen = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(5):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s)values' \
                                '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                                % ('院校名称', '省份', year, type, pici, beizhu, zuidifen,
                                    schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'])
                        self.cur.execute(sql)
                        d = {}
            if no is 23:
                no = '黑龙江'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidifen = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    diyi = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    dier = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    disan = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(8):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                                '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                                % ('院校名称', '省份', year, type, pici, beizhu, zuidifen, diyi, dier, disan,
                                    schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'])
                        self.cur.execute(sql)
                        d = {}

            if no is 31:
                no = '上海'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    renke = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    shuxue = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    waiyu = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    yuwen = selector.xpath('//table/thead/tr/th[9]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(9):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                            '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                            % ('院校名称', '省份', year, type, pici, beizhu, renke, zuidi, shuxue, waiyu, yuwen,
                                schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'])
                        self.cur.execute(sql)
                        d = {}
            if no is 32:
                no = '江苏省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    xuance = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    xingbie = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    fuzhu = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(8):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, xuance, xingbie, zuidi, fuzhu,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'])
                        self.cur.execute(sql)
                        d = {}
            if no is 33:
                no = '浙江省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zhixing = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    toudang = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    mingci = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(7):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, zhixing, toudang, mingci,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'])
                        self.cur.execute(sql)
                        d = {}

            if no is 34:
                no = '安徽省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    zuidipaiming = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(6):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, zuidi, zuidipaiming,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'])
                        self.cur.execute(sql)
                        d = {}
            if no is 35:
                no = '福建省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    zhiyuan = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(6):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, zuidi, zhiyuan,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'])
                        self.cur.execute(sql)
                        d = {}

            if no is 36:
                no = '江西省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuigao = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    pingjun = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(7):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, zuigao, zuidi, pingjun,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'])
                        self.cur.execute(sql)
                        d = {}
            if no is 37:
                no = '山东省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    jihua = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    toudang = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    touchu = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    zuigao = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[9]/text()')[0]
                    weici = selector.xpath('//table/thead/tr/th[10]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(10):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, jihua, toudang, touchu, zuigao, zuidi, weici,
                        schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'], d['9'])
                        self.cur.execute(sql)
                        d = {}
            if no is 41:
                no = '河南省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    jihua = selector.xpath('//table/thead/tr/th[5]')[0].xpath('string(.)')
                    jihuashu = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    toudang = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    xian = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    bili = selector.xpath('//table/thead/tr/th[9]')[0].xpath('string(.)')
                    zuidi = selector.xpath('//table/thead/tr/th[10]')[0].xpath('string(.)')
                    yu = selector.xpath('//table/thead/tr/th[11]/text()')[0]
                    shu = selector.xpath('//table/thead/tr/th[12]/text()')[0]
                    wai = selector.xpath('//table/thead/tr/th[13]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(13):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\'' \
                              ',\'%s\',\'%s\',\'%s\');' % ('院校名称', '省份', year, type, pici, beizhu, jihua, jihuashu,
                              toudang, xian, bili, zuidi, yu, shu, wai, schoolname, no, d['0'], d['1'], d['2'], d['3'],
                                d['4'], d['5'], d['6'], d['7'], d['8'], d['9'], d['10'], d['11'], d['12'])
                        self.cur.execute(sql)
                        d = {}

            if no is 42:
                no = '湖北省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(5):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' % ('院校名称', '省份', year, type,
                               pici, beizhu, zuidi, schoolname, no, d['0'],d['1'], d['2'], d['3'], d['4'])
                        self.cur.execute(sql)
                        d = {}
            if no is 43:
                no = '湖南省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    leixing = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    toudang = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    yu = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    shu = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    wai = selector.xpath('//table/thead/tr/th[9]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(9):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                                '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                                % ('院校名称', '省份', year, type, pici, leixing, beizhu, toudang, yu, shu, wai,
                            schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'])
                        self.cur.execute(sql)
                        d = {}

            if no is 44:
                no = '广东省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    jihua = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    toudang = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    fenshu = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    paiwei = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(8):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, jihua, toudang, fenshu, paiwei,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'])
                        self.cur.execute(sql)
                        d = {}
            if no is 45:
                no = '广西省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(5):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s)values' \
                            '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                            % ('院校名称', '省份', year, type, pici, beizhu, zuidi,
                                schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'])
                        self.cur.execute(sql)
                        d = {}
            if no is 46:
                no = '海南省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    jihua = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    toudang = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(7):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, jihua, toudang, zuidi,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'])
                        self.cur.execute(sql)
                        d = {}
            if no is 50:
                no = '重庆'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    leixing = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    jihua = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    luqu = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    zuigao = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[9]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(9):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, leixing, beizhu, jihua, luqu, zuigao, zuidi,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'])
                        self.cur.execute(sql)
                        d = {}
            if no is 52:
                no = '贵州省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    jihua = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    bili = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    toudangshu = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    zuigao = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[9]/text()')[0]
                    weici = selector.xpath('//table/thead/tr/th[10]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(10):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                        % ('院校名称', '省份', year, type, pici, beizhu, jihua, bili, toudangshu, zuigao, zuidi, weici,\
                        schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'], d['9'])
                        self.cur.execute(sql)
                        d = {}
            if no is 53:
                no = '云南省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    renshu = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    zuigao = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(7):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, renshu,zuigao, zuidi, \
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'])
                        self.cur.execute(sql)
                        d = {}

            if no is 61:
                no = '陕西省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    renshu = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    shiji = selector.xpath('//table/thead/tr/th[6]')[0].xpath('string(.)')
                    zuidi = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    weici = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(8):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, renshu, shiji, zuidi, weici, \
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'])
                        self.cur.execute(sql)
                        d = {}
            if no is 62:
                no = '甘肃省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(5):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, zuidi,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'])
                        self.cur.execute(sql)
                        d = {}
            if no is 63:
                no = '青海省'
                print no
                selector = etree.HTML(content.decode('utf8'))
                if selector.xpath('//table/tbody/tr'):
                    year = selector.xpath('//table/thead/tr/th[1]/text()')[0]
                    type = selector.xpath('//table/thead/tr/th[2]/text()')[0]
                    pici = selector.xpath('//table/thead/tr/th[3]/text()')[0]
                    beizhu = selector.xpath('//table/thead/tr/th[4]/text()')[0]
                    zuigao = selector.xpath('//table/thead/tr/th[5]/text()')[0]
                    zuigaoM = selector.xpath('//table/thead/tr/th[6]/text()')[0]
                    zuidi = selector.xpath('//table/thead/tr/th[7]/text()')[0]
                    zuidiM = selector.xpath('//table/thead/tr/th[8]/text()')[0]
                    renshu = selector.xpath('//table/thead/tr/th[9]/text()')[0]
                    content = selector.xpath('//table/tbody/tr')
                    d = {}
                    for each in content:
                        for i in range(9):
                            if each.xpath('td[' + str(i + 1) + ']/text()'):
                                d[str(i)] = each.xpath('td[' + str(i + 1) + ']/text()')[0]
                            else:
                                d[str(i)] = ''
                        sql = 'insert into new_各校各省历年录取(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)values' \
                              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % ('院校名称', '省份', year, type, pici, beizhu, zuigao, zuigaoM, zuidi, zuidiM, renshu,
                                 schoolname, no, d['0'], d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'])
                        self.cur.execute(sql)
                        d = {}


#看来此处仍然不能用 is 只能 ==
if __name__ == '__main__':

    f = getEachCollegeAccessNum()
    f.doSearchAllCollege()
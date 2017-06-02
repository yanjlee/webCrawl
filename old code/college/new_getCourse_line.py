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


class getEachCourseAccessLine():
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
                        'Host': 'gkcx.eol.cn'}
        self.session = requests.session()
        self.province = {
            '10003': '北京', '10000': '上海', '10011': '广东', '10006': '天津', '10028': '重庆', '10021': '湖北', '10005': '四川',
            '10016': '河北', '10017': '河南', '10009': ' 山东', '10010': '山西', '10014': '江苏', '10029': '陕西', '10018': '浙江',
            '10015': '江西', '10012': '广西', '10022': '湖南', '10027': '辽宁', '10008': '安徽', '10024': '福建', '10026': '贵州',
            '10023': '甘肃', '10004': '吉林', '10019': '海南', '10001': '云南', '10013': '新疆', '10007': '宁夏', '10025': '西藏',
            '10030': '青海', '10002': '内蒙古', '10031': '黑龙江', '10020': '香港', '10145': '澳门', '10146': '台湾'
        }
        self.kelei = {
            '10034': '文科', '100350': '理科', '10090': '综合', '10091': '艺术类', '10093': '体育类'
        }
        self.year = [2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008]
        self.track = open('track_0111', 'w')
    def setupsession(self):
        r = self.session.get('http://gkcx.eol.cn/', headers=self.headers, timeout=10)
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
        self.cur.execute('select count(*) from 所有高校')
        self.total_school = self.cur.fetchone()[0]
        return self.getUrl()

    def getUrl(self):
        self.wrong_url = []
        for i in range(int(self.total_school)):
            self.cur.execute("select schoolid,schoolname from 所有高校 where id =" + str(i + 1))
            reslut = self.cur.fetchone()
            if reslut:
                id = reslut[0]
                scn = reslut[1]
                print '第', i + 1, '所学校',scn
                self.constructUrl(id, scn)
                break
                time.sleep(1)

        self.conn.close()
    def constructUrl(self,id ,scn):
        for t in self.kelei.keys():
            for p in self.province.keys():
                for y in self.year:
                    url = 'http://gkcx.eol.cn/schoolhtm/specialty/' + id + '/' + t + '/specialtyScoreDetail' \
                                                                                     '_' + str(y) + '_' + p + '.htm'
                    self.getData(url, scn, self.province[p])
                    print '抓取', scn, self.province[p], self.kelei[t], y
                    time.sleep(1)

    def getData(self, url, scn, p):
        try:
            selector = etree.HTML(self.session.get(url, headers=self.headers, timeout=10).content)
            if selector.xpath('//div[@class="Scores"]/div[@class="S_result"]/table/tr[2]/td[2]/text()'):
                info = selector.xpath('//div[@class="Scores"]/div[@class="S_result"]/table/tr')
                for each_info in info:
                    if each_info.xpath('td[1]/text()'):
                        course_name = each_info.xpath('td[1]/text()')[0].replace(' ', '')
                    else:
                        course_name = ''
                    if each_info.xpath('td[2]/text()'):
                        year = each_info.xpath('td[2]/text()')[0]
                    else:
                        year = ''
                    if each_info.xpath('td[3]/text()'):
                        ave = each_info.xpath('td[3]/text()')[0]
                    else:
                        ave = ''
                    if each_info.xpath('td[4]/text()'):
                        max = each_info.xpath('td[4]/text()')[0]
                    else:
                        max = ''
                    if each_info.xpath('td[5]/text()'):
                        min = each_info.xpath('td[5]/text()')[0]
                    else:
                        min = ''
                    if each_info.xpath('td[6]/text()'):
                        s_type = each_info.xpath('td[6]/text()')[0].\
                            replace('                                                    \r\n                              '
                                    '                          ', '')\
                            .replace('\r\n                                                    ', '')
                    else:
                        s_type = ''
                    if each_info.xpath('td[7]/text()'):
                        admission_type = each_info.xpath('td[7]/text()')[0].\
                        replace('                                                    \r\n                                 '
                                '                       ', '').\
                        replace('\r\n                                                    ', '')
                    else:
                        admission_type = ''
                    if year:
                        SQL = 'insert into new_course_line (院校名称,专业名称,年份,省份,平均分,最高分,最低分,考生类别,录取批次)' \
                              'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                              % (scn, course_name, year, p, ave, max, min, s_type, admission_type)
                        self.cur.execute(SQL)
                    self.conn.commit()
        except:
            print '请求错误', url, p, scn
            text = url, ', ', scn, ', ', p, '\n'
            self.track.writelines(text)

if __name__ == '__main__':
    g = getEachCourseAccessLine()
    g.setupsession()





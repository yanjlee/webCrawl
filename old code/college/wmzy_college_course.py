# -*-coding:utf8-*-
'''
抓取各大学在各省的招生专业
def __init__(self) 这个初始化函数可以扔到后面
'''
import requests
import random
import MySQLdb
import re
import sys
reload(sys)
sys.setrecursionlimit(2000000)

sys.setdefaultencoding('utf-8')

class getEachCollegeCourseInfo():
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
        self.cur.execute('set sql_safe_updates=0;')

    def setupsession(self):
        #先把sc_id和sch_id从数据库提取出来
        sql = 'select * from ex_college_info'
        self.cur.execute(sql)
        list = self.cur.fetchall()
        for each in list:
            cname = each[1]
            ctype = each[2]
            sch_id = each[3]
            sc_id = each[8]
            self.do_redict(cname, ctype, sch_id, sc_id)

    def do_redict(self, cname, ctype, sch_id, sc_id):
        year = [2015, 2016]
        wenli = ['wen', 'li']
        province = ['安徽', '黑龙江', '吉林', '辽宁', '河北', '河南', '内蒙古', '天津', '山东', '湖北', '湖南', '山西', '陕西',
                    '江西', '浙江', '江苏', '上海', '四川', '贵州', '云南', '重庆', '广西', '广东', '福建', '海南', '甘肃', '宁夏',
                    '新疆', '青海']
        if ctype == '本科':
            t = 7
        elif ctype == '专科':
            t = 5
        url = 'http://www.wmzy.com/api/school/getAllMajorInfo'
        for p in province:
            for y in year:
                for k in wenli:
                    params = {
                        'sch_id': sch_id,
                        '_sch_id': sc_id,
                        'diploma': t,
                        'diploma_id': '7',
                        'province': p,
                        'year': y,
                        'ty': k,
                        '': '',
                        'major_type': '1',
                        '_': '1486445460324'
                    }
                    print cname, ctype, y, p, k
                    self.get_data(self.session.get(url, params=params).content, cname, ctype, k, y, p)
                    self.conn.commit()

    def get_data(self, content, cname, ctype, k, y, p):
        if k is 'wen':
            wenli = '文史'
        elif k is 'li':
            wenli = '理工'

        if re.findall('category-list(.*?)显示更多', content, re.S):
            if re.findall('category-hd(.*?)n</div',
                                   re.findall('category-list(.*?)显示更多', content, re.S)[0].replace(' ',''), re.S):
                for each in re.findall('category-hd(.*?)n</div',
                                       re.findall('category-list(.*?)显示更多', content, re.S)[0].replace(' ',''), re.S):
                    yiji = re.findall('>·(.*?)</div', each, re.S)[0]
                    for erji in re.findall('ahref(.*?)</a', each, re.S):
                        erji_1 = re.findall('">(.*)', erji, re.S)[0]
                        sql = 'insert into college_course_info(院校名称,本专科,年份,省份,文理科,一级学科,二级学科)values' \
                            '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                              % (cname, ctype, y, p, wenli, yiji, erji_1)
                        self.cur.execute(sql)
if __name__ == '__main__':
    c = getEachCollegeCourseInfo()
    c.setupsession()
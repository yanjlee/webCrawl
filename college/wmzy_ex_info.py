# -*-coding:utf8-*-
'''
get the informations which i never notice
'''

import requests
import random
import re
from lxml import etree
import MySQLdb
import sys
reload(sys)

sys.setrecursionlimit(2000000)

sys.setdefaultencoding('utf-8')

class theExInfos():
    def start(self):
        '''
        需要抓取,各个学校的10年收入增长,各个专业的10年收入增长,还有获取学校网址,以及学校简介
        :return:
        '''
        self.cur.execute('set sql_safe_updates=0;')
        return self.constructUrl()

    def constructUrl(self):
        self.cur.execute('select * from college_info;')
        n = 1
        for each in self.cur.fetchall():
            college = each[1]
            ctype = each[3]
            url = each[7]
            print n
            self.inputData(self.session.get(url).content, college, ctype)
            self.conn.commit()
            n += 1
        self.cur.execute('select * from course_rank;')
        # for each in self.cur.fetchall():
        #     url = each[5]
        #     print n
        #     self.inputData_2(self.session.get(url).content, url)
        #     self.conn.commit()
        #     n += 1

        self.conn.close()
    def inputData(self, content, cname, ctype):
        # selector = etree.HTML(content)
        # if selector.xpath('//ul[@class="attr"]/li[1]/text()'):
        #     info_1 = selector.xpath('//ul[@class="attr"]/li[1]/@title')[0]
        #     info_2 = selector.xpath('//ul[@class="attr"]/li[2]/@title')[0].replace(' ', '').replace('\n', '')\
        #         .replace('<p>', '').replace('</p>', '')
        #     info_3 = selector.xpath('//ul[@class="attr"]/li[3]/@title')[0].replace(' ', '').replace('\n', '')\
        #         .replace('<p>', '').replace('</p>', '')
        # else:
        #     info_1 = ''
        #     info_2 = ''
        #     info_3 = ''
        # sql_1 = 'update college_info set %s=\'%s\'where %s=\'%s\' and %s=\'%s\';' \
        #       % ('网址', info_1, '院校名称', cname, '本专科', ctype)
        # sql_2 = 'update college_info set %s=\'%s\'where %s=\'%s\' and %s=\'%s\';' \
        #         % ('地址', info_2,'院校名称', cname, '本专科', ctype)
        # sql_3 = 'update college_info set %s=\'%s\'where %s=\'%s\' and %s=\'%s\';' \
        #         % ('电话', info_3, '院校名称', cname, '本专科', ctype)
        # self.cur.execute(sql_1)
        # self.cur.execute(sql_2)
        # self.cur.execute(sql_3)
        if re.findall('PageData(.*?)catch', content, re.S):
            text = re.findall('PageData(.*?)catch', content, re.S)[0]
            benxiao = re.findall('employment(.*?)provinceSal', text, re.S)[0]
            ben = ''
            if re.findall('grad_year(.*?)}', benxiao, re.S):
                for each1 in re.findall('grad_year(.*?)}', benxiao, re.S):
                    year1 = re.findall('":(.*?),"salary', each1, re.S)[0]
                    salary1 = re.findall('salary":(.*?),"virtual', each1, re.S)[0]
                    ben += '第' + year1 + '年月薪为 '+ salary1 + ','
                sql_b = 'update ex_college_info set %s=\'%s\' where %s=\'%s\' and %s=\'%s\';' \
                      % ('本校十年薪酬', ben, '院校名称', cname, '本专科', ctype)
                self.cur.execute(sql_b)
            quanguo = re.findall('provinceSal(.*?)ind', text, re.S)[0]
            quan = ''
            if re.findall('grad_year(.*?)', quanguo, re.S):
                for each2 in re.findall('grad_year(.*?)}', quanguo, re.S):
                    year2 = re.findall('":(.*?),"salary', each2, re.S)[0]
                    salary2 = re.findall('salary":(.*?),"sample_coun', each2, re.S)[0]
                    quan += '第' + year2 + '年月薪为'+ salary2 + '元,'
                sql_q = 'update ex_college_info set %s=\'%s\' where %s=\'%s\' and %s=\'%s\';' \
                      % ('全国十年薪酬', quan, '院校名称', cname, '本专科', ctype)
                self.cur.execute(sql_q)

    def inputData_2(self, content, url):
        if re.findall('PageData(.*?)catch', content, re.S):
            text = re.findall('PageData(.*?)catch', content, re.S)[0]
            benxiao = re.findall('employment(.*?)countrySal', text, re.S)[0]
            ben = ''
            if re.findall('grad_year(.*?)}', benxiao, re.S):
                for each_1 in re.findall('grad_year(.*?)}', benxiao, re.S):
                    year_1 = re.findall('":(.*?),"salary', each_1, re.S)[0]
                    salary_1 = re.findall('salary":(.*?),"virtual', each_1, re.S)[0]
                    ben += '第' + year_1 + '年月薪为 ' + salary_1 + '元,'
                sql_b = 'update course_rank set %s=\'%s\' where %s=\'%s\';' \
                        % ('本专业十年薪酬', ben, 'url', url, )
                self.cur.execute(sql_b)
            quanguo = re.findall('countrySal(.*?)ind', text, re.S)[0]
            quan = ''
            if re.findall('grad_year(.*?)', quanguo, re.S):
                for each_2 in re.findall('grad_year(.*?)}', quanguo, re.S):
                    year_2 = re.findall('":(.*?),"salary', each_2, re.S)[0]
                    salary_2 = re.findall('salary":(.*?),"sampl', each_2, re.S)[0]
                    quan += '第' + year_2 + '年月薪为' + salary_2 + '元,'
                sql_q = 'update course_rank set %s=\'%s\' where %s=\'%s\';' \
                        % ('全国十年薪酬', quan, 'url', url,)
                self.cur.execute(sql_q)
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
        #设定一个请求头的UA
        self.headers = {'User-Agent': random.choice(self.user_agent_list),
                        'Host': 'www.wmzy.com'}
        #cookie包含账号信息
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
if __name__ == '__main__':
    c = theExInfos()
    c.start()
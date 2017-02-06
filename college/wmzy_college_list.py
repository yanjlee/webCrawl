# -*-coding:utf8-*-
'''
抓取一个2500所大学的基本信息
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

class collegeInfo():
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
        #论证页面是否为空
        self.K = False
        #创建mysql链接
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
        # r = self.session.get('http://www.wmzy.com/api/school?tool')
        # print r.content
        return self.getCollegeList()
    def getCollegeList(self):
        url = 'http://www.wmzy.com/api/school/getSchList'
        '''
        在requests里使用get请求时候，参数是用params,而post请求时,参数是用data
        '''
        n = 1
        while(True):
            params_benke = {
                #这个是本科的
                'diploma': 7,
                'province_filter': '',
                'city_filter': '',
                'school_type': '',
                'major_second_category_filter': '',
                'major_filter': '',
                'sch_name_pattern': '',
                'page': n,
                'count': 100,
                'sort_by': 'zonghe',
                'score': 'false',
                'diploma_id': 7,
                '_': 1486258064982
            }
            params_zhuanke = {
                # 这个是专科的
                'diploma': 5,
                'province_filter': '',
                'city_filter': '',
                'school_type': '',
                'major_second_category_filter': '',
                'major_filter': '',
                'sch_name_pattern': '',
                'page': n,
                'count': 100,
                'sort_by': 'xinchou',
                'score': 'false',
                'diploma_id': 7,
                '_': 1486266150958
            }
            '''
            这里的本专科手动来调整
            '''
            self.do_clear_zhuanke(self.session.get(url, params=params_zhuanke).content)

            # self.do_clear_benke(self.session.get(url, params=params_benke).content)
            if self.K:
                n += 1
                continue
            elif self.K is False:
                break
        #一切完毕,断开mysql链接
        self.conn.close()
    def do_clear_benke(self, content):
        '''
        这里作为本科数据清洗,提取出需要的信息，大学的url
        :param content:
        :return: 如果信息为空，返回，并break
        '''
        # print content.replace(' ', '')
        text = re.findall('tbody(.*?)\</tbody', content.replace(' ', ''), re.S)[0]
        if re.findall('\<tdclass=(.*?)\</tr\>', text, re.S):
            self.K = True
            list = re.findall('\<tdclass=(.*?)\</tr\>', text, re.S)
            for each in list:
                # print each
                sc_name = re.findall('html(.*?)a', each, re.S)[0].replace('\\">', '').replace('</', '')
                type = re.findall('\<span\>(.*?)\</span\>', each, re.S)[0]
                location = re.findall('\<td\>(.*?)\</td\>', each, re.S)[1]
                provide_type = re.findall('\<td\>(.*?)\</td\>', each, re.S)[2].replace('/', '及')
                commit = re.findall('n(.*?)n', re.findall('col4td(.*)', each, re.S)[0], re.S)[0].replace('\\', '')
                url = 'http://www.wmzy.com' \
                      + re.findall('href=(.*?)"\>', each, re.S)[0].replace('\\"', '').replace('\\', '')
                sql = 'insert into college_info(院校名称,类型,所在地,提供学位,综合评价,url,本专科)' \
                      'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                      % (sc_name, type, location, provide_type, commit, url, '本科')
                self.cur.execute(sql)
                self.conn.commit()

        else:
            self.K = False
    def do_clear_zhuanke(self, content):
        '''
        这里作为专科数据清洗,提取出需要的信息，大学的url
        :param content:
        :return: 如果信息为空，返回，并break
        '''
        text = re.findall('tbody(.*?)\</tbody', content.replace(' ', ''), re.S)[0]
        if re.findall('\<tdclass=(.*?)\</tr\>', text, re.S):
            self.K = True
            list = re.findall('\<tdclass=(.*?)\</tr\>', text, re.S)
            for each in list:
                sc_name = re.findall('diploma=5(.*?)a', each, re.S)[0].replace('\\">', '').replace('</', '')
                type = re.findall('\<span\>(.*?)\</span\>', each, re.S)[0]
                location = re.findall('\<td\>(.*?)\</td\>', each, re.S)[1]
                provide_type = re.findall('\<td\>(.*?)\</td\>', each, re.S)[2].replace('/', '及')
                if re.findall('\d{1,10}元', each, re.S):
                    daiyu = re.findall('\d{1,10}元', each, re.S)[0]
                else: daiyu = ''
                url = 'http://www.wmzy.com' \
                      + re.findall('href=(.*?)"\>', each, re.S)[0].replace('\\"', '').replace('\\', '')
                sql = 'insert into college_info(院校名称,类型,所在地,提供学位,毕业五年月薪,url,本专科)' \
                      'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                      % (sc_name, type, location, provide_type, daiyu, url, '专科')
                # print sql
                self.cur.execute(sql)
            self.conn.commit()

        else:
            self.K = False

    def getInfo(self):
        '''
        从数据库里读取大学的url
        :return: self.getData(content)
        '''
        sql = 'select * from college_info;'
        self.cur.execute(sql)
        text = self.cur.fetchall()
        self.cur.execute('set sql_safe_updates=0')
        n = 1
        for each in text:
            sc_name = each[1]
            url = each[7]
            # print sc_name, url
            self.getData(self.session.get(url).content, url, sc_name, n)
            #一个学校结束再commit()
            self.conn.commit()
            n += 1


        #循环结束
        self.conn.close()

    def getData(self, content, url, sname, n):
        print n, sname
        selector = etree.HTML(content)
        text = selector.xpath('//ul[@class="block-list"]/li')
        # print text
        for each in text:
            title = each.xpath('div[@class="block-title"]/text()')[0].replace('(', '').replace(')', '')
            contents = each.xpath('div[@class="block-fd"]')[0]
            info = contents.xpath('string(.)').replace(' ', '').replace('\n', '').replace('￥', '')
            if title == '男女比例10年':
                title = '男女比例近3年'
            # print title, info
            sql = 'update college_info set %s=\'%s\' where url=\'%s\';' % (title, info, url)
            self.cur.execute(sql)

if __name__ == '__main__':
    c = collegeInfo()
    # c.setupsession()
    c.getInfo()

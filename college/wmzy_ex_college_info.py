# -*-coding:utf8-*-
'''
抓取各学校详细信息
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

class getEachCollegeExInfo():
    def setupsession(self):
        sql = 'select * from college_info ;'
        self.cur.execute(sql)
        text = self.cur.fetchall()
        n = 1
        for each in text:
            sc_name = each[1]
            sc_type = each[3]
            sc_url = each[7]
            print n
            self.getData(self.session.get(sc_url).content, sc_name, sc_type)
            #为表更新sc_id
            sc_id = each[7].replace('http://www.wmzy.com/api/school/', '').replace('.html', '')
            # sql = 'update ex_college_info set sc_id=\'%s\' where 院校名称=\'%s\' and 本专科=\'%s\';' \
            #       % (sc_id, sc_name, sc_type)
            # self.cur.execute(sql)
            self.conn.commit()
            n += 1

        self.conn.close()
    def getData(self, content, s_name, type):
        '''
        获取学校的 sch_id 基本简介,知名校友,毕业生去向,毕业生分布
        :param content: 网页html
        :param name: 学校名称
        :param type: 本专科,用来区分
        :return:
        '''
        text = re.findall('PageData(.*?)catch', content, re.S)[0]
        #获取学校sch_id
        sch_id = re.findall('"sch_id":"(.*?)"', text, re.S)[0]
        #获取就业案例
        if re.findall('{"mate_name":(.*?)}]}',
                                    re.findall('"excellent"(.*?)"schoolFamous', text, re.S)[0], re.S):
            for each in re.findall('{"mate_name":(.*?)}]}',
                                    re.findall('"excellent"(.*?)"schoolFamous', text, re.S)[0], re.S):
                name = re.findall('(.*?)gender', each, re.S)[0].replace('"', '')
                sex = re.findall('gender(.*?)grad', each, re.S)[0].replace('":"', '').replace('","', '')
                grad_date = re.findall('grad_date(.*?)grad_sch', each, re.S)[0].replace('":"', '').replace('","', '')
                job_item = re.findall('"item_id"(.*?)job_seq', each, re.S)
                job = ''
                for eachjob in job_item:
                    c_name = re.findall('inc_name(.*?)inc_scale', eachjob, re.S)[0].\
                            replace('":"', '').replace('","', '').replace('\'', '')
                    industry = re.findall('"inc_industry(.*?)inc_industry_id"', eachjob, re.S)[0].\
                            replace('":"', '').replace('","', '')
                    time_s = re.findall('start_time(.*?)end_time', eachjob, re.S)[0].\
                            replace('":"', '').replace('","', '')
                    time_e = re.findall('end_time(.*?)job_sal', eachjob, re.S)[0].\
                            replace('":"', '').replace('","', '')
                    position = re.findall('position(.*)', eachjob, re.S)[0].\
                            replace('":"', '').replace('","', '')
                    salary = re.findall('"job_sal(.*?)jobSalary', eachjob, re.S)[0].\
                            replace('":"', '').replace('","', '')
                    job += '公司名称:' + c_name + ',行业:' + industry + ',职位:' + position + ',收入:' + salary +\
                               ',时间:' + time_s + '-' + time_e + '/'
                jobInfo = '姓名:' + name + ',性别:' + sex + ',毕业时间:' + grad_date + '/' + job + ';'
        else:
            jobInfo = ''
        #获取知名校友
        fam = ''
        if re.findall('schoolFamous(.*?)employment', text, re.S):
            for eachFamous in re.findall('sch_mate(.*?)"}',
                                             re.findall('schoolFamous(.*?)employment', text, re.S)[0], re.S):
                fname = re.findall('"(.*?)pos', eachFamous, re.S)[0].replace('","', '').replace(':"', '')
                postion = re.findall('position(.*)', eachFamous, re.S)[0].\
                        replace('":"', '').replace('，', ',').replace('、', '')
                fam += '姓名:' + fname + ',' + postion + ';'
        else: fam = ''

        #抓行业
        han = ''
        if re.findall('ind(.*?)"loc"', text, re.S):
            for eachHangye in re.findall('ind_name(.*?)}', re.findall('ind(.*?)"loc"', text, re.S)[0], re.S):
                hangye = re.findall(':"(.*?)"."ratio', eachHangye, re.S)[0]
                ratio = re.findall('ratio":(.*)', eachHangye, re.S)[0]
                han += hangye + ratio + '%;'
        else: han = ''
        #毕业生分布
        bi = ''
        if re.findall('"loc"(.*?)male_ratio', text, re.S):
            for eachbiye in re.findall('city_name(.*?)}', re.findall('"loc"(.*?)male_ratio', text, re.S)[0], re.S):
                city = re.findall('":"(.*?)","loc_x"', eachbiye, re.S)[0]
                b_ratio = re.findall('_ratio":(.*?),"ratio', eachbiye, re.S)[0]
                bi += city + b_ratio + '%;'
        else: bi = ''

        sql = 'insert into ex_college_info(院校名称,本专科,sch_id,就业案例,知名校友,毕业生行业分布,毕业生地区分布)values' \
              '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (s_name, type, sch_id, jobInfo, fam, han, bi)
        # print sql
        self.cur.execute(sql)
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

if __name__ == '__main__':
    c = getEachCollegeExInfo()
    c.setupsession()
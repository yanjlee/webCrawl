# -*-coding:utf8-*-
'''
这个网站反爬虫是，先通过一个url post数据，然后服务器修改cookie，在数据访问时候，
服务器调取cookie里信息，完成对数据的提取和输出
'''

import requests
import MySQLdb
import random
import time
import re
import sys
reload(sys)


sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000000)


class getScoreDataFromWM():
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

        self.headers = {'Host': 'www.wmzy.com',
                        'User-Agent': random.choice(self.user_agent_list)
                        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        #创建mysql链接
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        self.wrongData = open('wrongData', 'w')
    def dealTheData(self):
        #年份编码
        self.year = [2015, 2014, 2013]
        #各省的编码
        self.province = {
            # 51: '四川',
            33: '浙江', 34: '安徽', 11: '北京', 50: '重庆', 35: '福建', 44: '广东', 52: '贵州',
            62: '甘肃', 45: '广西', 41: '河南', 42: '湖北', 23: '黑龙江', 46: '海南', 43: '湖南', 13: '河北',
            22: '吉林', 32: '江苏', 36: '江西', 21: '辽宁', 64: '宁夏', 15: '内蒙古', 63: '青海', 14: '山西',
            31: '上海', 61: '陕西', 37: '山东', 12: '天津', 65: '新疆', 53: '云南'
                        }
        #录取批次的编码
        self.access_type = {
            'bk1': '本科第一批',
            'bk2': '本科第二批',
            'bk3': '本科第三批',
            'bk2a': '本科第二批A类',
            'bk2b': '本科第二批B类',
            'bk3a': '本科第三批A类',
            'bk3b': "本科第三批B类",
            'zk1': '专科第一批',
            'zk2': '专科第二批'
        }
        #文理科的编码
        self.wenli = {'w': '文史', 'l': '理工'}
        for y in self.year:
            for p in self.province.keys():
                for t in self.wenli.keys():
                    for i in range(100, 750):
                        self.dealTheCookies(y, p, t, i)
                        # time.sleep(1)
                        print str(y), self.province[p], self.wenli[t], str(i)

        print '抓取完毕'
        #修改录取批次的名字
        sql_safe = 'set sql_safe_updates=0'
        self.cur.execute(sql_safe)
        for key in self.access_type.keys():
            sql = 'update 同分考生去向 set 录取批次=\'' + self.access_type[key] + '\' where 录取批次=\'' + key + '\';'
            self.cur.execute(sql)
            self.conn.commit()

        print '清洗完毕'
        self.conn.close()


    def dealTheCookies(self, year, prov, type, score):
        url_post = 'http://www.wmzy.com/zhiyuan/score?'
        data = {
            'prov': prov, #省的代码
            'pici': 'bk1',  #经测试，这里可以不修改
            'hasScore': 'true',
            'realScore': score,
            'scoreRank': '',
            'score': 0,
            'ty': type,  #这里是文理分科,理科是l，文科是w
            'score_form': 'scoreBox'
        }
        self.session.cookies.update(self.session.post(url_post, data=data).cookies)
        self.getData(year, prov, type, score)
    def getData(self, year, prov, type, score):
        try:
            url = 'http://www.wmzy.com/tongfen?year=' + str(year)
            text = self.session.get(url).content
            # print text
            #先判断数据存在不存在
            if re.findall('"majors":\[(.*?)]},"yearList":', text, re.S)[0]:
                contents = re.findall('"majors":\[(.*?)]},"yearList":', text, re.S)[0]

                # print content
                cons = re.findall('{"sch_id"(.*?)}', contents, re.S)
                # print len(con)
                for con in cons:
                    # print i
                    # wenli = re.findall('"wenli":"(.*?)","score"', con, re.S)[0]
                    sc_name = re.findall('"sch_name":"(.*?)","major_id"', con, re.S)[0]
                    c_name = re.findall('"major_name":"(.*?)","wenli"', con, re.S)[0]
                    c_cate = re.findall('"major_cate":"(.*?)","major_batch"', con, re.S)[0]
                    score = re.findall('"score":(.*?),"score_rank"', con, re.S)[0]
                    s_rank = re.findall('"score_rank":(.*?),"major_cate"', con, re.S)[0]
                    ac_num = re.findall('enroll_count":(\d{1,3})', con, re.S)[0]
                    pici = re.findall('"major_batch":"(.*?)","diploma"', con, re.S)[0]
                    # print sc_name, c_name, c_cate, score, s_rank, ac_num, pici
                    sql = 'insert into 同分考生去向(省份,年份,录取批次,科类,学校名称,专业名称,专业类别,分数,位次,录取人数)' \
                            'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' \
                            % (self.province[prov], year, pici, self.wenli[type], sc_name, c_name, c_cate,
                                score, s_rank, ac_num)
                    # print sql
                    self.cur.execute(sql)
                self.conn.commit()
        except:
            print '请求错误'
            data = str(year), prov, type, score
            self.wrongData.writelines(data)



if __name__ == '__main__':
    c = getScoreDataFromWM()
    c.dealTheData()







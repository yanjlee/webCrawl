# -*-coding:utf8 -*-

import requests
import json
import time
import MySQLdb
import sys
reload(sys)


sys.setdefaultencoding('utf-8')
sys.setrecursionlimit(2000000)

class getAllColleges():
    def __init__(self):
        object.__init__(self)
        headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'gkcx.eol.cn',
        }
        self.session = requests.session()
        self.session.headers.update(headers)
    def setupsession(self):
        r = self.session.get('http://gkcx.eol.cn/')
        cookies = r.cookies
        self.session.cookies.update(cookies)
        #建立mysql链接
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        return self.getAllColleges(r.content)
    def getAllColleges(self, content):

        '''
        一共2750所大学
        api接口是: http://data.api.gkcx.eol.cn/soudaxue/queryschool.html?messtype=json&schooltype=&size=50&page=1
        '''
        api = "http://data.api.gkcx.eol.cn/soudaxue/queryschool.html?messtype=json&schooltype=&size=50&page="
        #一共2750条数据，每页max是50条，一共50页
        for i in range(55):
            print '第' + str(i+1) +'页'
            jsContent = self.session.get(api + str(i+1)).content
            jsDict = json.loads(jsContent)['school']
            for i in range(len(jsDict)):
                schoolid = jsDict[i]['schoolid']                    #学校id
                schoolname = jsDict[i]['schoolname']                #校名
                f985 = jsDict[i]['f985']                            #非985
                f211 = jsDict[i]['f211']                            #非211
                thelevel = jsDict[i]['level']                       #层次 本科/专科
                schooltype = jsDict[i]['schooltype']                #学校类型
                membership = jsDict[i]['membership']                #隶属于
                schoolproperty = jsDict[i]['schoolproperty']        #性质
                shoufei = jsDict[i]['shoufei']                      #收费
                jianjie = jsDict[i]['jianjie']                      #学校简介
                SQL = 'insert into all_college (schoolid,schoolname,f985,f211,thelevel,schooltype,' \
                      'membership,schoolproperty,shoufei,jianjie)' \
                  'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                  %(schoolid,schoolname,f985,f211,thelevel,schooltype,membership,schoolproperty,shoufei,jianjie)
                self.cur.execute(SQL)
                self.conn.commit()
            time.sleep(1)

        print '录入完毕'
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    d = getAllColleges()
    d.setupsession()
# -*- coding:utf8 -*-
'''
我只是把用正则表达式的方式把这个脚本补齐，这个网页通过脚本打开，中文里显示是乱码，通过.decode('utf-8'),也不可以
我实际上是通过网页的查看html来录入数据的
'''
import requests
import time
import MySQLdb
from lxml import etree
import sys
import re
reload(sys)


sys.setdefaultencoding('utf-8')

class allHighSchool():
    def __init__(self):
        headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'gz.gaokao789.com',
        'Referer': 'http://gz.gaokao789.com/'
        }
        self.session = requests.session()
        self.session.headers.update(headers)
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

    def setupsession(self):
        #一共31个省
        for i in range(31):
            print '抓取第', i, '个省'
            url = 'http://gz.gaokao789.com/diqu.asp?sid=' + str(i+1)
            # self.getData(etree.HTML(self.session.get(url).content))
            self.getre(self.session.get(url).content)
            time.sleep(3)

    def getData(self, selector):
        pass
        '''
        用xpath很蛋疼，是html结构的问题，读出来的数据问题很大，果断弃之，用正则表达式
        '''
        # prov_name = selector.xpath('//body/table[6]/tr/td/span[2]/text()')[0].replace(' ','').replace('>>', '')
        # city_name = selector.xpath('//body/table[8]/tr/td[3]/table[1]/tr/td/text()')[0]
        # area_name = selector.xpath('//body/table[8]/tr/td[3]/table[3]/tr/td[1]/span/text()')[0]

    def getre(self, text):
        # text = open('demo1').read()
        prov_name = re.findall('首页&nbsp;</a><span class="xihei">&gt;&gt;&nbsp;(.*?)</span></td>', text, re.S)
        city_name = re.findall('<td height="24" align="center" valign="middle" class="baicu">(.*?)</td>', text, re.S)
        part = re.findall('<table width="100%" border="0" cellpadding="0" cellspacing="0" bgcolor="50C5F9">(.*?)'
                          '<td height="7"></td>', text, re.S)

        for i in range(len(city_name)):
            area_name = re.findall('class="xihei"><span class="STYLE2">(.*?)</span></td>', part[i], re.S)
            content = re.findall('<table width="100%" border="0" cellpadding="2" '
                                 'cellspacing="1" bgcolor="93C0EA">(.*?)</table></td>', part[i], re.S)
            # print len(area_name), len(content)
            for a in range(len(area_name)):
                c = content[a]
                lists = re.findall('lass="lred2" target="_blank">(.*?)</a></td>', c, re.S)
                for u in lists:
                    if u == '':
                        continue
                    else:
                        # self.inserData(prov_name[0], city_name[i], area_name[a], u.replace('' ,''))
                        # self.conn.commit()
                        print prov_name[0],city_name[i], area_name[a], u.replace('' ,'')

        print 'done'

    def inserData(self, p, c, a, u):
        SQL = 'insert into 全国高中统计(省份,城市,区城镇,学校名称)values(\'%s\',\'%s\',\'%s\',\'%s\');'%(p, c, a, u)
        self.cur.execute(SQL)
if __name__ == '__main__':
    c = allHighSchool()
    c.setupsession()
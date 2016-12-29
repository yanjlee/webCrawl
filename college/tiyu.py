# -*-coding:utf8 -*-

import requests
import time
import random
import MySQLdb
from lxml import etree
import sys
reload(sys)


sys.setdefaultencoding('utf-8')

class tiyusheng():
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

        self.headers = {'Host': 'gaokao.chsi.com.cn',
                        'User-Agent': random.choice(self.user_agent_list)
                        }
        self.session = requests.session()

    def setupsession(self):
        r = self.session.get('http://gaokao.chsi.com.cn/zsgs/gspydyzgmd--method-groupByYx,year-2016.dhtml',
                             headers=self.headers, timeout=10)
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
        #创建表
        SQL = 'create table 2016年高水平运动队名单(id int auto_increment primary key,姓名 nvarchar(100),性别 nvarchar(100),' \
                    '所在省份 nvarchar(100),毕业学校 nvarchar(100),拟录取学校名称 nvarchar(100),测试项目 nvarchar(100),' \
              '证书等级 nvarchar(100),考试类型 nvarchar(100), 测试成绩 nvarchar(100), ' \
              '合格规则 nvarchar(100),测试合格标准 nvarchar(100),录取优惠分值 nvarchar(100),备注 nvarchar(500));'
        self.cur.execute(SQL)
        self.conn.commit()
        return self.geturls(r.content)

    # def getUrl(self, content):
    #     selector = etree.HTML(content)
    #     content = selector.xpath('//table[@class="mrg_auto bg_color03"]/tr/td')
    #     print content
    #     for each in content:
    #         if each.xpath('td/a'):
    #             url = each.xpath('td/a/@href')[0]
    #             title = each.xpath('td/a/text()')[0]
    #             self.geturls(url, title)
    #             print url, title
    #     self.conn.commit()

    def geturls(self, content):
        selector = etree.HTML(content)
        if selector.xpath('//div[@class="clearfix"]/ul/li'):
            s_url = selector.xpath('//div[@class="clearfix"]/ul/li')
            for each in s_url:
                link = each.xpath('a/@href')[0]
                # school = each.xpath('a/text()')[0]
                self.getdata(link)
                time.sleep(2)


    def getdata(self, url):
        URL = 'http://gaokao.chsi.com.cn' + url
        selector = etree.HTML(self.session.get(URL).content)
        content = selector.xpath('//*[@id="YKTabCon2_10"]/tr')
        for each in content:
            if each.xpath('td[@width="80"]'):
                continue
            else:
                name = each.xpath('td[1]/text()')[0]
                sex = each.xpath('td[2]/text()')[0]
                belong = each.xpath('td[3]/text()')[0]
                schoolname = each.xpath('td[4]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                ac_school = each.xpath('td[5]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                proj = each.xpath('td[6]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                zhengshu = each.xpath('td[7]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                type = each.xpath('td[8]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                chengji = each.xpath('td[9]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                hege = each.xpath('td[10]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                biaozhun = each.xpath('td[11]/div/a/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                youhui = each.xpath('td[12]/text()')[0].replace('\r', '').replace('\n', '').replace(' ', '').replace('\t', '')
                if each.xpath('td[13]/div/a/text()'):
                    beizhu = each.xpath('td[13]/div/a/@title')[0]
                else:
                    beizhu = ''
                sql = 'insert into 2016年高水平运动队名单(姓名,性别,所在省份,毕业学校,拟录取学校名称,测试项目,证书等级,考试类型,测试成绩' \
                      ',合格规则,测试合格标准,录取优惠分值,备注)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                      % (name, sex, belong, schoolname, ac_school, proj,
                         zhengshu, type, chengji, hege, biaozhun, youhui, beizhu)
                print sql
                self.cur.execute(sql)
        self.conn.commit()

if __name__ == '__main__':
    b = tiyusheng()
    b.setupsession()
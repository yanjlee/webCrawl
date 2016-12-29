# -*- coding:utf8 -*-
import requests
import MySQLdb
from lxml import etree
import sys
import time



reload(sys)
sys.setdefaultencoding('utf8')

class p_rank():
    def __init__(self):
        headers = {
            'Host': 'kaoyan.eol.cn',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
        }
        self.session = requests.session()
        self.session.headers.update(headers)
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()

    def setupsessoion(self):
        urls = [
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386238.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386275_1.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386281_1.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386289_1.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386299_1.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386341.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386358_1.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386391.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386411.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386432.shtml',
        'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386448.shtml'
        ]
        for url in urls:
            print '录入中...'
            self.getdata(etree.HTML(self.session.get(url).content))
            self.conn.commit()
            time.sleep(3)
        print '抓取结束'
        self.conn.close()
    def getdata(self, selector):
        title = selector.xpath('/html/body/div[6]/div[1]/div[1]/p[1]/text()')
        print title[0]
        # SQL_data = 'create table %s (id int auto_increment primary key,名次 nvarchar(10),学校名称 nvarchar(20),所在地区 nvarchar(20),' \
        #            '总分 nvarchar(10),全国排名 nvarchar(10),星级排名 nvarchar(10),办学层次 nvarchar(10))' % (title[0])
        # print '建表中...'
        # # self.cur.execute(SQL_data)
        # # self.conn.commit()
        # content = selector.xpath('//*[@id="mcontent"]/div[1]/table/tbody/tr')
        # for each_info in content:
        #     if each_info.xpath('td/b/text()'):
        #         print each_info.xpath('td/b/text()')[0]
        #     else:
        #         rank = each_info.xpath('td[1]/text()')[0]
        #         if each_info.xpath('td[2]/a/text()'):
        #             name = each_info.xpath('td[2]/a/text()')[0]
        #         elif each_info.xpath('td[2]/text()'):
        #             name = each_info.xpath('td[2]/text()')[0]
        #         area = each_info.xpath('td[3]/text()')[0]
        #         num = each_info.xpath('td[4]/text()')[0]
        #         rank_q = each_info.xpath('td[5]/text()')[0]
        #         rank_star = each_info.xpath('td[6]/text()')[0]
        #         s_class = each_info.xpath('td[7]/text()')[0]
        #         SQL = 'insert into %s (名次,学校名称,所在地区,总分,全国排名,星级排名,办学层次)values' \
        #               '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
        #               % (title[0], rank, name, area, num, rank_q, rank_star, s_class)
        #         self.cur.execute(SQL)
        #         self.conn.commit()

if __name__ == '__main__':
    c = p_rank()
    c.setupsessoion()
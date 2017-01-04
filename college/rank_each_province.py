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
        print '建表中...',
        SQL_data = 'create table 各省高校排名 (id int auto_increment primary key,省份 nvarchar(20),名次 nvarchar(10),学校名称' \
                   ' nvarchar(20),所在地区 nvarchar(20),全国名次 nvarchar(10),总分 nvarchar(10),办学类型 nvarchar(20)' \
                   ',星级排名 nvarchar(10),办学层次 nvarchar(10))'
        self.cur.execute(SQL_data)
        self.conn.commit()
    def setupsessoion(self):
        urls = [
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386469.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386483.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386513.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386532.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386543.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386554.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386563.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386571.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386583.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386588.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386594.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386607.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386627.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386639.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386649.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386665.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386666.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386667.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386669.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386670.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386671.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386672.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386674.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386676.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386679.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386687.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386693.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386695.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386702.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386713.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160413_1386730.shtml'

        ]
        for url in urls:
            print '录入中...'
            self.getdata(etree.HTML(self.session.get(url).content))
            self.conn.commit()
            time.sleep(3)
        print '抓取结束'
        self.conn.close()
    def getdata(self, selector):
        title = selector.xpath('/html/body/div[6]/div[1]/div[1]/p[1]/text()')[0].replace('，', ',')\
            .replace('最佳大学排行榜', '').replace('2016', '')
        T = title.split(',')[0]
        print '录入',T
        content = selector.xpath('//*[@id="mcontent"]/div[1]/table/tbody/tr')
        for each_info in content:
            if each_info.xpath('td/b/text()'):
                continue
            else:
                rank = each_info.xpath('td[1]/text()')[0]
                if each_info.xpath('td[2]/a/text()'):
                    name = each_info.xpath('td[2]/a/text()')[0]
                elif each_info.xpath('td[2]/text()'):
                    name = each_info.xpath('td[2]/text()')[0]
                area = each_info.xpath('td[3]/text()')[0]
                rank_g = each_info.xpath('td[4]/text()')[0]
                num = each_info.xpath('td[5]/text()')[0]
                type = each_info.xpath('td[6]/text()')[0]
                rank_star = each_info.xpath('td[7]/text()')[0]
                s_class = each_info.xpath('td[8]/text()')[0]
                SQL = 'insert into 各省高校排名 (名次,省份,学校名称,所在地区,全国名次,总分,办学类型,星级排名,办学层次)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                      % (rank, T, name, area,rank_g, num, type, rank_star, s_class)
                print SQL
                self.cur.execute(SQL)


if __name__ == '__main__':
    c = p_rank()
    c.setupsessoion()
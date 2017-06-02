# -*-coding:utf8-*-

import requests
import MySQLdb
from lxml import etree
import sys
import time



reload(sys)
sys.setdefaultencoding('utf8')

class rank():
    def __init__(self):
        headers = {
        'Host': 'kaoyan.eol.cn',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
        }
        self.session = requests.session()
        self.session.headers.update(headers)
        #建立mysql连接
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
    def setupsessoion_rank1_400(self):
        urls = [
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1385922.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1385964.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386018.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386022.shtml'
        ]
        for url in urls:
            print '录入中...'
            self.getdata(etree.HTML(self.session.get(url).content))
            self.conn.commit()
            time.sleep(3)
        print '抓取结束'
        self.conn.close()
    def getdata(self, selector):
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
                type = each_info.xpath('td[3]/text()')[0]
                area = each_info.xpath('td[4]/text()')[0]
                total = each_info.xpath('td[5]/text()')[0]
                train = each_info.xpath('td[6]/text()')[0]
                science = each_info.xpath('td[7]/text()')[0]
                society = each_info.xpath('td[8]/text()')[0]
                s_type = each_info.xpath('td[9]/text()')[0]
                star_rank = each_info.xpath('td[10]/text()')[0]
                s_class = each_info.xpath('td[11]/text()')[0]

                SQL = 'insert into college_rank1_700(名次,学校名称,类型,所在地,总分,人才培养,科学研究,社会影响,' \
                      '办学类型,星级排名,办学层次)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                      %(rank, name, type, area, total, train, science, society, s_type, star_rank, s_class)
                self.cur.execute(SQL)
    def setupsessoion_other(self):
        urls = [
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386168.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386180.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386184.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386122.shtml',
            'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386153.shtml'
        ]
        for url in urls:
            print '抓取中....'
            self.getdata_2(etree.HTML(self.session.get(url).content))
            time.sleep(4)
        print '抓取完毕'
        self.conn.close()
    def getdata_2(self, selector):
        title = selector.xpath('/html/body/div[6]/div[1]/div[1]/p[1]/text()')
        SQL_data = 'create table %s (id int auto_increment primary key,名次 nvarchar(10),学校名称 nvarchar(20),所在地区 nvarchar(20),' \
                   '奖励数 nvarchar(10),全国排名 nvarchar(10),星级排名 nvarchar(10),办学层次 nvarchar(10))'%(title[0])
        print '建表中...'
        self.cur.execute(SQL_data)
        self.conn.commit()
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
                num = each_info.xpath('td[4]/text()')[0]
                rank_q = each_info.xpath('td[5]/text()')[0]
                rank_star = each_info.xpath('td[6]/text()')[0]
                s_class = each_info.xpath('td[7]/text()')[0]
                SQL = 'insert into %s (名次,学校名称,所在地区,奖励数,全国排名,星级排名,办学层次)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                      %(title[0], rank, name, area, num, rank_q, rank_star, s_class)
                self.cur.execute(SQL)
                self.conn.commit()
if __name__ == '__main__':
    r = rank()
    r.setupsessoion_rank1_400()
    # r.setupsessoion_other()
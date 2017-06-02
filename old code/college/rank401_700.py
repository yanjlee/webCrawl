# -*- coding:utf8 -*-

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
            'Host': 'gaokao.xdf.cn',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
        }
        self.session = requests.session()
        self.session.headers.update(headers)
        # 建立mysql连接
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='college_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
    def setupsessions(self):
        urls = [
            # 'http://gaokao.xdf.cn/201601/10414735.html',
            'http://gaokao.xdf.cn/201601/10414736.html',
            'http://gaokao.xdf.cn/201601/10414737.html'
        ]
        for url in urls:
            print '录入中...'
            self.getdata(etree.HTML(self.session.get(url).content))
            time.sleep(3)

        self.conn.close()
        print '抓取完毕'

    def getdata(self, selector):
        '''
        网站相当恶心，第一个网址和第二个网址抓取内容相似，但是html结构不同.
        '''
        # content = selector.xpath('//div[@class="air_con f-f0"]/b/div/b/table/tbody/tr')
        content = selector.xpath('//div[@class="air_con f-f0"]/b/div/table/tbody/tr')
        for each_info in content:
            rank = each_info.xpath('td[1]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            name = each_info.xpath('td[2]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            type = each_info.xpath('td[3]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            area = each_info.xpath('td[4]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            total = each_info.xpath('td[5]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            train = each_info.xpath('td[6]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            science = each_info.xpath('td[7]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            society = each_info.xpath('td[8]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            s_type = each_info.xpath('td[9]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            star_rank = each_info.xpath('td[10]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')
            s_class = each_info.xpath('td[11]/p/text()')[0].replace('\n\t\t\t\t\t\t', '').replace('\n\t\t\t\t\t', '')

            SQL = 'insert into college_rank1_700(名次,学校名称,类型,所在地,总分,人才培养,科学研究,社会影响,' \
                    '办学类型,星级排名,办学层次)values' \
                    '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                    % (rank, name, type, area, total, train, science, society, s_type, star_rank, s_class)
            self.cur.execute(SQL)
            self.conn.commit()

if __name__ == '__main__':
    c = rank()
    c.setupsessions()
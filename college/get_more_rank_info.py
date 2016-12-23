# -*-coding:utf8-*-

import requests
import MySQLdb
from lxml import etree
import sys




reload(sys)
sys.setdefaultencoding('utf8')

class get_more_rank_info():
    def __init__(self):
        headers = {
            'Host': 'kaoyan.eol.cn',
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
        self.selector = etree.HTML(self.session.get('http://www.eol.cn/html/ky/16phb/index.html').content)
    def get_danxiangbang(self):
        # content = self.selector.xpath('//div[@class="conBox dxb"]/div[@class="dxbTab"]')
        title1 = self.selector.xpath('//div[@class="conBox dxb"]/div[@class="dxbTab"]/div[1]/div[1]/div/h1/a/text()')[0]
        title2 = self.selector.xpath('//div[@class="conBox dxb"]/div[@class="dxbTab"]/div[2]/div[1]/div/h1/a/text()')[0]
        title3 = self.selector.xpath('//div[@class="conBox dxb"]/div[@class="dxbTab"]/div[3]/div[1]/div/h1/a/text()')[0]
        # SQL_D1 = 'create table %s (id int auto_increment primary key,学校名称 nvarchar(20),所在地区 nvarchar(20),全国排名' \
        #          ' nvarchar(10),办学类型 nvarchar(20),星级排名 nvarchar(10),办学层次 nvarchar(20))'%(title1)
        # SQL_D2 = 'create table %s (id int auto_increment primary key,学校名称 nvarchar(20),所在地区 nvarchar(20),' \
        #          '得分 nvarchar(10),全国排名 nvarchar(10),星级排名 nvarchar(10),办学层次 nvarchar(20))'%(title2)
        # SQL_D3 = 'create table %s (id int auto_increment primary key,学校名称 nvarchar(20),所在地区 nvarchar(20),' \
        #          '2015世界排名平均位次 nvarchar(10),2015世界排名次数 nvarchar(10),全国排名 nvarchar(10),星级排名 nvarchar(10),办学层次 nvarchar(20))' \
        #          ''%(title3)
        # self.cur.execute(SQL_D1)
        # self.cur.execute(SQL_D2)
        # self.cur.execute(SQL_D3)
        # self.conn.commit()
        # content1 = self.selector.xpath('//div[@class="conBox dxb"]/div[@class="dxbTab"]/div[1]/div[2]/div/table/tr')
        # for each in content1:
        #     if each.xpath('th/text()'):
        #         continue
        #     else:
        #         name = each.xpath('td[2]/a/text()')[0]
        #         area = each.xpath('td[3]/text()')[0]
        #         rank = each.xpath('td[4]/text()')[0]
        #         type = each.xpath('td[5]/text()')[0]
        #         rank_star = each.xpath('td[6]/text()')[0]
        #         s_class = each.xpath('td[7]/text()')[0]
        #         sql = 'insert into %s(学校名称,所在地区,全国排名,办学类型,星级排名,办学层次)' \
        #               'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(title1,name,area,rank,type,rank_star,s_class)
        #         self.cur.execute(sql)
        #         self.conn.commit()
        # content2 = self.selector.xpath('//div[@class="conBox dxb"]/div[@class="dxbTab"]/div[2]/div[2]/div/table/tr')
        # for each in content2:
        #     if each.xpath('th/text()'):
        #         continue
        #     else:
        #         name = each.xpath('td[2]/a/text()')[0]
        #         area = each.xpath('td[3]/text()')[0]
        #         mark = each.xpath('td[4]/text()')[0]
        #         rank = each.xpath('td[5]/text()')[0]
        #         rank_star = each.xpath('td[6]/text()')[0]
        #         s_class = each.xpath('td[7]/text()')[0]
        #         sql = 'insert into %s(学校名称,所在地区,得分,全国排名,星级排名,办学层次)' \
        #               'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (
        #               title2, name, area, mark,rank, rank_star, s_class)
        #         self.cur.execute(sql)
        #         self.conn.commit()
        # content3 = self.selector.xpath('//div[@class="conBox dxb"]/div[@class="dxbTab"]/div[3]/div[2]/div/table/tr')
        # for each in content3:
        #     if each.xpath('th/text()'):
        #         continue
        #     else:
        #         if each.xpath('td[2]/a/text()'):
        #             name = each.xpath('td[2]/a/text()')[0]
        #         elif each.xpath('td[2]/text()'):
        #             name = each.xpath('td[2]/text()')[0]
        #         area = each.xpath('td[3]/text()')[0]
        #         rank1 = each.xpath('td[4]/text()')[0]
        #         rank2 = each.xpath('td[5]/text()')[0]
        #         rank = each.xpath('td[6]/text()')[0]
        #         rank_star = each.xpath('td[6]/text()')[0]
        #         s_class = each.xpath('td[7]/text()')[0]
        #         sql = 'insert into %s(学校名称,所在地区,2015世界排名平均位次,2015世界排名次数,全国排名,星级排名,办学层次)' \
        #               'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (
        #                   title3, name, area, rank1, rank2, rank, rank_star, s_class)
        #         self.cur.execute(sql)
        #         self.conn.commit()
        # self.conn.close()

        url_1 = 'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386043_1.shtml'
        url_2 = 'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386061.shtml'
        url_3 = 'http://kaoyan.eol.cn/bao_kao/re_men/201604/t20160412_1386068.shtml'
        selector1 = etree.HTML(self.session.get(url_1).content)
        selector2 = etree.HTML(self.session.get(url_2).content)
        selector3 = etree.HTML(self.session.get(url_3).content)
        content1 = selector1.xpath('//*[@id="mcontent"]/div[1]/table/tbody/tr')
        content2 = selector2.xpath('//*[@id="mcontent"]/div[1]/table/tbody/tr')
        content3 = selector3.xpath('//*[@id="mcontent"]/div[1]/table/tbody/tr')
        print '1'
        for each in content1:
            if each.xpath('td/b/text()'):
                continue
            else:
                if each.xpath('td[2]/a/text()'):
                    name = each.xpath('td[2]/a/text()')[0]
                elif each.xpath('td[2]/text()'):
                    name = each.xpath('td[2]/text()')[0]
                area = each.xpath('td[3]/text()')[0]
                rank = each.xpath('td[4]/text()')[0]
                type = each.xpath('td[5]/text()')[0]
                rank_star = each.xpath('td[6]/text()')[0]
                s_class = each.xpath('td[7]/text()')[0]
                sql = 'insert into %s(学校名称,所在地区,全国排名,办学类型,星级排名,办学层次)' \
                      'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(title1,name,area,rank,type,rank_star,s_class)
                self.cur.execute(sql)
                self.conn.commit()
        print '2'
        for each in content2:
            if each.xpath('td/b/text()'):
                continue
            else:
                if each.xpath('td[2]/a/text()'):
                    name = each.xpath('td[2]/a/text()')[0]
                elif each.xpath('td[2]/text()'):
                    name = each.xpath('td[2]/text()')[0]
                area = each.xpath('td[3]/text()')[0]
                mark = each.xpath('td[4]/text()')[0]
                rank = each.xpath('td[5]/text()')[0]
                rank_star = each.xpath('td[6]/text()')[0]
                s_class = each.xpath('td[7]/text()')[0]
                sql = 'insert into %s(学校名称,所在地区,得分,全国排名,星级排名,办学层次)' \
                        'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (
                        title2, name, area, mark,rank, rank_star, s_class)
                self.cur.execute(sql)
                self.conn.commit()
        print '3'
        for each in content3:
            if each.xpath('td/b/text()'):
                continue
            else:
                if each.xpath('td[2]/a/text()'):
                    name = each.xpath('td[2]/a/text()')[0]
                elif each.xpath('td[2]/text()'):
                    name = each.xpath('td[2]/text()')[0]
                area = each.xpath('td[3]/text()')[0]
                rank1 = each.xpath('td[4]/text()')[0]
                rank2 = each.xpath('td[5]/text()')[0]
                rank = each.xpath('td[6]/text()')[0]
                rank_star = each.xpath('td[6]/text()')[0]
                s_class = each.xpath('td[7]/text()')[0]
                sql = 'insert into %s(学校名称,所在地区,2015世界排名平均位次,2015世界排名次数,全国排名,星级排名,办学层次)' \
                        'values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (
                            title3, name, area, rank1, rank2, rank, rank_star, s_class)
                self.cur.execute(sql)
                self.conn.commit()

        self.conn.close()

if __name__ == '__main__':
    c = get_more_rank_info()
    c.get_danxiangbang()
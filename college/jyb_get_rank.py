# -*-coding:utf8-*-


import requests
import MySQLdb
import re
from lxml import etree
import sys
reload(sys)
sys.setrecursionlimit(2000000)
sys.setdefaultencoding('utf-8')

def run():
    session = requests.session()
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'www.chinadegrees.cn'
    }
    session.headers.update(headers)
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='454647',
        db='college_info',
        charset="utf8"
    )
    cur = conn.cursor()
    url = 'http://www.chinadegrees.cn/webrms/pages/Ranking/xkpmGXZJ.jsp'
    r = session.get(url).content
    selector = etree.HTML(r)
    categories = selector.xpath('//div[@class="PageBody"]/table/tr/td[1]/p')
    for c in categories:
        c_name = c.xpath('a/text()')[0].replace(' ', '')
        url_1 = 'http://www.chinadegrees.cn/webrms/pages/Ranking/' + c.xpath('a/@href')[0]
        r_2 = session.get(url_1).content
        selector_2 = etree.HTML(r_2)
        categories_2 = selector_2.xpath('//div[@class="PageBody"]/table/tr/td[2]/div/table/tr/td/p')
        # print categories_2
        for c_2 in categories_2:
            c_name2 = re.findall('\d (.*)', c_2.xpath('a/text()')[0], re.S)[0]
            url_2 = 'http://www.chinadegrees.cn/webrms/pages/Ranking/' + c_2.xpath('a/@href')[0]
            r_3 = session.get(url_2).content.replace('&nbsp;', '')
            selector_3 = etree.HTML(r_3)
            categories_3 = selector_3.xpath('//div[@class="PageBody"]/table/tr/td[3]/table/tr[4]/td/div/table/tr')
            num = 0
            for c_3 in categories_3:
                name = re.findall('\d{5}(.*)', c_3.xpath('td[1]/div/text()')[0], re.S)[0]
                if c_3.xpath('td[2]/text()'):
                    socre = c_3.xpath('td[2]/text()')[0]
                    num = socre
                else:
                    socre = num
                sql = 'insert into 学科得分(年份,第一大类,第二大类,院校名称,得分)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                      % (2012, c_name, c_name2, name, socre)
                print sql
                cur.execute(sql)
                conn.commit()

    conn.close()

def run2009():
    session = requests.session()
    headers = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Host': 'www.chinadegrees.cn'
    }
    session.headers.update(headers)
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='454647',
        db='college_info',
        charset="utf8"
    )
    cur = conn.cursor()
    selector = etree.HTML(session.get('http://www.chinadegrees.cn/webrms/Services/xkpm.jsp').content)
    categories_1 = selector.xpath('//body/div[@class="BOX"]/table[1]/tr[1]/td')
    for c_1 in categories_1:
        c_name = c_1.xpath('a/text()')[0].replace(' ', '')
        url_1 = 'http://www.chinadegrees.cn/webrms/Services/' + c_1.xpath('a/@href')[0]
        # print c_name, url_1
        selector_2 = etree.HTML(session.get(url_1).content)
        categories_2 = selector_2.xpath('//body/div[@class="BOX"]/table[1]/tr[2]/td/table/tr/td')
        for c_2 in categories_2:
            c_name2 = re.findall('\d (.*)', c_2.xpath('span/a/text()')[0], re.S)[0]
            url_2 = 'http://www.chinadegrees.cn/webrms/Services/' + c_2.xpath('span/a/@href')[0]
            # print url_2
            selector_3 = etree.HTML(session.get(url_2).content)
            categories_3 = selector_3.xpath('//body/div[@class="BOX"]/table[3]/tr/td[2]/table/tr')
            num = 0
            for c_3 in categories_3:
                if c_3.xpath('td[2]'):
                    # name = c_3.xpath('td[2]/text()')[0]
                    name = re.findall('\d (.*)', c_3.xpath('td[2]/text()')[0], re.S)[0]
                    if c_3.xpath('td[3]/text()'):
                        socre = c_3.xpath('td[3]/text()')[0]
                        num = socre
                    else:
                        socre = num
                    sql = 'insert into 学科得分(年份,第一大类,第二大类,院校名称,得分)values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                          % (2009, c_name, c_name2, name, socre)
                    print sql
                    cur.execute(sql)
                    conn.commit()

    conn.close()

run2009()

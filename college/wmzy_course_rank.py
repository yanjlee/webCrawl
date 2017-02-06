# -*-coding:utf8-*-
'''
抓取各学科排名
发现在setupsession里,关于代码表述有更简洁的的方式相比前一个脚本
'''
import requests
import random
import MySQLdb
import re
from lxml import etree
import sys
reload(sys)
sys.setrecursionlimit(2000000)

sys.setdefaultencoding('utf-8')

class getEachCourseRank():
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

        self.headers = {'User-Agent': random.choice(self.user_agent_list),
                        'Host': 'www.wmzy.com'}
        self.cookies = {
            'Cookie': 'guide=1;'
                      ' sessionid=s:EsEpQkmCHUXEct7jVHKXwLyK.fm+4BeS95NUVpu9+8nr1nrrgLb+jWt6PbEp1UHLeErk;'
                      ' _gat=1;'
                      ' Hm_lvt_02ceb62d85182f1a72db7d703affef9c=1485224333,1485274811,1486178337,1486257750;'
                      ' Hm_lpvt_02ceb62d85182f1a72db7d703affef9c=1486257782;'
                      ' _ga=GA1.2.41898681.1485053816;'
                      ' Hm_lvt_8a2f2a00c5aff9efb919ee7af23b5366=1485224333,1485274811,1486178338,1486257750;'
                      ' Hm_lpvt_8a2f2a00c5aff9efb919ee7af23b5366=1486257858'
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.session.cookies.update(self.cookies)
        # 论证页面是否为空
        self.K = False
        # 创建mysql链接
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='454647',
            db='wmzy_info',
            charset="utf8"
        )
        self.cur = self.conn.cursor()
        #本专科
        self.benzhuanke = {7: '本科', 5: '专科'}
    def setupsession(self):
        url = 'http://www.wmzy.com/api/rank/major'
        n = 1
        while (True):
            for i in self.benzhuanke.keys():
                params = {
                    'diploma': i,
                    'majorCategory': '',
                    'page': n,
                    'type': 'xinchou',
                    'count': 100,
                    'diploma_id': 7,
                    '_': 1486359623000
                }
                self.do_clear(self.session.get(url, params=params).content, self.benzhuanke[i])
                self.conn.commit()
            if self.K:
                n += 1
                continue
            elif self.K is False:
                break
        #抓取完毕，断开连接
        self.conn.close()
    def do_clear(self, content, benzhaunke):
        text = re.findall('tbody(.*?)\</tbody', content.replace(' ', ''), re.S)[0]
        # print text
        if re.findall('<tdclass=(.*?)</tr>', text, re.S):
            self.K = True
            list = re.findall('<tdclass=(.*?)</tr>', text, re.S)
            for each in list:
                rank = re.findall('\d{1,4}</', re.findall('"><spanclass=(.*?)span></span>',
                                                          each, re.S)[0])[0].replace('</', '')
                if benzhaunke == '本科':
                    c_name = re.findall('html(.*?)</a>', each, re.S)[0].replace('\\">', '')
                elif benzhaunke == '专科':
                    c_name = re.findall('diploma=5(.*?)a', each, re.S)[0].replace('\\">', '').replace('</', '')
                type = re.findall('<td>(.*?)</td>', each, re.S)[1]
                salary = re.findall('<td>(.*?)</td>', each, re.S)[2].replace('\\n', '').replace('￥', '')
                url = 'http://www.wmzy.com' \
                      + re.findall('href=(.*?)">', each, re.S)[0].replace('\\"', '').replace('\\', '')
                sql = 'insert into course_rank(本专科,排名,专业名称,专业类别,毕业五年后月薪,url)values' \
                      '(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' % (benzhaunke, rank, c_name, type, salary, url)
                # print sql
                self.cur.execute(sql)
        else:
            self.K = False

    def do_update(self):
        self.cur.execute('set sql_safe_updates=0;')
        sql = 'select * from course_rank where id>=1164'
        self.cur.execute(sql)
        list = self.cur.fetchall()
        for each in list:
            id = each[0]
            url = each[5]
            input_d = ''
            input_g = ''
            input_c = ''
            input_q = ''
            self.do_getData(self.session.get(url).content, url, input_d, input_g, input_c, input_q, id)
            self.conn.commit()
        #更新完毕
        self.conn.close()
    def do_getData(self, content, url, input_d, input_g, input_c, input_q, id):
        '''
        这个页面要获取 基本信息,专业介绍,毕业生行业分布,毕业生岗位分布,毕业生公司分布,毕业生地区分布
        :param content:
        :param url:
        :return:
        '''
        print id
        selector = etree.HTML(content)
        #获取基本信息
        text = selector.xpath('//ul[@class="block-list"]/li')
        for each in text:
            title = each.xpath('div[@class="block-title"]/text()')[0].replace('(', '').replace(')', '')
            if title == '男女比例10年':
                t = '男女比例近3年'
            else:
                t = title
            contents = each.xpath('div[@class="block-fd"]')[0]
            info = contents.xpath('string(.)').replace(' ', '').replace('\n', '').replace('￥', '')
            sql_1 = 'update course_rank set %s=\'%s\' where url=\'%s\';' % (t, info, url)
            self.cur.execute(sql_1)
        #专业介绍
        if selector.xpath('//div[@class="des"]/p/text()'):
            introduction = selector.xpath('//div[@class="des"]/p/text()')[0]
        else:
            introduction = selector.xpath('//div[@class="des"]')[0]\
                .xpath('string(.)').replace('\n', '').replace('\'', '')
        sql_2 = 'update course_rank set 基本信息=\'%s\' where url=\'%s\';' % (introduction, url)
        self.cur.execute(sql_2)
        #毕业生行业分布
        data = re.findall('params(.*?)catch', content, re.S)[0]
        fenbu = re.findall('"ind"(.*?)"zhineng_dis"', data, re.S)[0]
        fenbu_list = re.findall('ind_name(.*?)}', fenbu, re.S)
        for each in fenbu_list:
            category = re.findall(':"(.*?)",', each, re.S)[0]
            ratio = re.findall('"ratio":(.*)', each, re.S)[0]
            input_d += category + ' ' + ratio + ','
        sql_3 = 'update course_rank set 毕业生行业分布=\'%s\' where url=\'%s\';' % (input_d, url)
        self.cur.execute(sql_3)
        #毕业生岗位分布
        gangwei = selector.xpath('//div[@class="sch-mod sch-position fun"]/div/div/div/ul/li')
        for each in gangwei:
            name = each.xpath('h2/text()')[0]
            position = each.xpath('p[1]')[0].xpath('string(.)')
            hangye = each.xpath('p[2]')[0].xpath('string(.)')
            input_g += name + ',' + position + ',' + hangye +';'
        sql_4 = 'update course_rank set 毕业生岗位分布=\'%s\' where url=\'%s\';' % (input_g, url)
        self.cur.execute(sql_4)
        #毕业生公司分布
        gongsi = selector.xpath('//div[@class="sch-mod sch-inc"]/div/table/tbody/tr')
        for each in gongsi:
            name = each.xpath('td/a/text()')[0].replace('\n', '').replace(' ', '')
            property = each.xpath('td[3]/text()')[0]
            input_c += name + ',' + property + ';'
        sql_5 = 'update course_rank set 毕业生公司分布=\'%s\' where url=\'%s\';' % (input_c, url)
        self.cur.execute(sql_5)
        #毕业生地区分布
        area_fenbu = re.findall('loc":(.*?)\|', data, re.S)[0]
        area_fenbu_list = re.findall('city_name":(.*?)}', area_fenbu, re.S)
        for each in area_fenbu_list:
            city = re.findall('"(.*?)","loc_x', each, re.S)[0]
            ratio = re.findall('"_ratio":(.*?),"ratio"', each, re.S)[0]
            input_q += city + ',' + ratio + ';'
        sql_6 = 'update course_rank set 毕业生地区分布=\'%s\' where url=\'%s\';' % (input_q, url)
        self.cur.execute(sql_6)

if __name__ == '__main__':
    c = getEachCourseRank()
    # c.setupsession()
    c.do_update()
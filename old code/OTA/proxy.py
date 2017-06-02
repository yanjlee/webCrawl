# coding=utf8

import requests
from lxml import etree
import time
import random
from OTA import user_agent_list

class getProxies():
    def __init__(self):
        user_agent = random.choice(user_agent_list)
        host = 'www.xicidaili.com'
        headers = {
            'User-Agent': user_agent,
            'Host': host,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        }
        self.session = requests.session()
        self.session.headers.update(headers)
        text = '%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s' \
        % ('国家', 'ip', 'prot', '服务器地址', '是否匿名', '方式', '速度', '链接时间', '存活时间', '测试时间')
        with open('proxy.txt', 'a')as f:
            f.writelines(text + '\n')
            f.close()
    def setupsession(self):
        '''
        这里抓取西刺前5页的代理ip
        '''
        for i in range(1, 6):
            url = 'http://www.xicidaili.com/nn/' + str(i)
            self.get_proxies(self.session.get(url).text)
            time.sleep(5)
    def get_proxies(self, content):
        '''
        这个页面获取代理信息,国家,ip,端口,速度
        :param content: 页面的html
        '''
        selector = etree.HTML(content)
        con = selector.xpath('//table/tr')
        for each in con:
            if each.xpath('th[1]'):
                continue
            else:
                if each.xpath('td[1]/img/@alt'):
                    country = each.xpath('td[1]/img/@alt')[0]
                else:
                    country = ''
                ip = each.xpath('td[2]/text()')[0]
                port = each.xpath('td[3]/text()')[0]
                if each.xpath('td[4]/a'):
                    area = each.xpath('td[4]/a/text()')[0]
                else:
                    area = ''
                nm = each.xpath('td[5]/text()')[0]
                type = each.xpath('td[6]/text()')[0]
                var = each.xpath('td[7]/div/@title')[0]
                time = each.xpath('td[8]/div/@title')[0]
                alive = each.xpath('td[9]/text()')[0]
                certify = each.xpath('td[10]/text()')[0]
                print(country, ip, port, area, nm, type, var, time, alive, certify)
                text = '%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001%s\u0001' \
                       % (country, ip, port, area, nm, type, var, time, alive, certify)
                with open('proxy.txt', 'a') as f:
                    f.writelines(text + '\n')

if __name__ == '__main__':
    c = getProxies()
    c.setupsession()
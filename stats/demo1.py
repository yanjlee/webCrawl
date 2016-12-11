# -*-coding:utf8 -*-

import requests
import re
from lxml import etree


def getdata():
    url = 'http://www.stats.gov.cn/tjsj/sjjd/201612/t20161209_1439302.html'
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        'Referer': 'http://www.stats.gov.cn/tjsj/zxfb/',
        'Host': 'www.stats.gov.cn'
    }
    r = requests.get(url, headers=headers)
    '''
    selector = etree.HTML(r.content)
    content = selector.xpath('//div[@class="center_xilan"]')[0]
    con = content.xpath('string(.)').replace('\n', '').replace('\t', '')
    print con
    这种方法是把字体都爬了下来
    '''
    con = re.search('<div class="center_xilan" style="min-height:400px;">(.*?)<div class="center_wenzhang">', r.content, re.S).group()
    content = re.findall('">(.*?)<', con, re.S)
    a = []
    for i in content:
        if i:
            a.append(i.replace('\t', '').replace('&nbsp', '').replace(' ','').replace('　　','\n'))
    b = ''
    for j in a:
        b +=j
    print b

if __name__ == '__main__':
    getdata()
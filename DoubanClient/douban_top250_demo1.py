# -*- coding:utf8 -*-
‘’‘
只是写了豆瓣电影TOP250爬去的框架，实现了翻页，还没有对数据进行处理，同时也没有爬去电影的海报
’‘’
import requests
from lxml import etree

class DoubanClient():
    def __init__(self):
        object.__init__(self)
        self.url = 'http://movie.douban.com/top250'
        self.headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Host': 'movie.douban.com'
        }
        
        self.session = requests.session()
        self.session.headers.update(self.headers)
        
    #创建session
    def setupsession(self):
        r = self.session.get(self.url, headers=self.headers)
        return self.get_data(r.content)


    def get_data(self, content):
        selector = etree.HTML(content)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            title = eachMovie.xpath('div[@class="hd"]/a/span/text()')
            full_title = ''
            for each in title:
                full_title += each
            movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()')[0].replace(' ','')
            star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
            #测试过程中发现有的电影没有quote，这里需要对他做一个判断，没有quote的则赋空值
            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
            if quote:
                quote = quote[0]
            else:
                quote = ''

        Paginator = selector.xpath('//span[@class="next"]/a/@href')
        #到最后一页没有数据，则对列表做一个判断
        if Paginator:
            paginator_url = 'http://movie.douban.com/top250'+Paginator[0]
            print paginator_url
            n = self.session.get(paginator_url, timeout=2)
            return self.nextPage(n.content)

        print 'it\'done'

    #接收数据翻页数据，返回给get_data
    def nextPage(self, content):
        return self.get_data(content)





if __name__ == '__main__':
    c = DoubanClient()
    c.setupsession()

# -*- coding:utf8 -*-

import requests
from lxml import etree
import pymongo

class DoubanClient():
    def __init__(self):
        object.__init__(self)
        self.url = 'http://movie.douban.com/top250'
        self.headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        'Host': 'movie.douban.com'
        }

        self.session = requests.session()
        self.session.headers.update(self.headers)
        self.connection = pymongo.MongoClient()


    def setupsession(self):
        r = self.session.get(self.url)
        #获取response的cookies作为后续请求的cookies
        self.cookies = r.cookies
        self.session.cookies.update(self.cookies)
        dbName =self.connection.Douban
        self.post_info = dbName.DoubanMovieTop250
        #创建链接时即创建数据库
        return self.get_data(r.content)

    def get_data(self, content):
        selector = etree.HTML(content)
        input_data = {}
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            title = eachMovie.xpath('div[@class="hd"]/a/span/text()')
            full_title = ''
            for each in title:
                full_title += each
            input_data['title'] = full_title

            input_data['movieInfo'] = eachMovie.xpath('div[@class="bd"]/p/text()')[0].replace(' ','')

            input_data['star'] = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]

            #测试过程中发现有的电影没有quote，这里需要对他做一个判断，没有quote的则赋空值

            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
            if quote:
                input_data['quote'] = quote[0]
            else:
                input_data['quote'] = ''
            # 因为数据插入是一条一条以字典的格式，并不是插入一个字典，因此每次插入后，应该重新定义字典
            self.post_info.insert(input_data)
            input_data = {}

        Paginator = selector.xpath('//span[@class="next"]/a/@href')
        #到最后一页没有数据，则对列表做一个判断
        if Paginator:
            paginator_url = 'http://movie.douban.com/top250'+Paginator[0]
            n = self.session.get(paginator_url)
            return self.nextPage(n.content)

        print 'it\'done'

    #接收数据翻页数据，返回给get_data
    def nextPage(self, content):
        return self.get_data(content)





if __name__ == '__main__':
    c = DoubanClient()
    c.setupsession()
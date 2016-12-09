# -*- coding:utf8 -*-
import requests
import pymongo
from multiprocessing.dummy import Pool
from lxml import etree


class Douban_book():
    def __init__(self):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Host': 'book.douban.com'
        }
        self.session = requests.session()
        self.session.headers.update(headers)
        self.connection = pymongo.MongoClient()

    def setupsession(self):
        url = 'http://book.douban.com/top250'
        r = self.session.get(url)
        cookies = r.cookies
        self.session.cookies.update(cookies)
        tdb = self.connection.Douban
        self.post = tdb.bookTop250
        selector = etree.HTML(r.content)
        total_page = selector.xpath('//*[@id="content"]/div/div[1]/div/div/a[9]/text()')[0]
        urls = []
        for i in range(int(total_page)):
            urls.append('https://book.douban.com/top250?start=' + str(i*25))
        return self.startTheThreadings(urls)

    def startTheThreadings(self, urls):
        pool = Pool(4)
        print '开始采集...'
        pool.map(self.getAllBooks, urls)
        pool.close()
        print '采集完毕'

    def getAllBooks(self, url):
        selector = etree.HTML(self.session.get(url).content)
        all_books = selector.xpath('//*[@id="content"]/div/div[1]/div/table')
        book = {}
        for each_book in all_books:
            book['title'] = each_book.xpath('tr[@class="item"]/td[@valign="top"]/div[@class="pl2"]/a/@title')[0]
            f_title = each_book.xpath('tr[@class="item"]/td[@valign="top"]/div[@class="pl2"]/span/text()')
            if f_title:
                book['f_title'] = f_title[0]
            book['info'] = each_book.xpath('tr[@class="item"]/td[@valign="top"]/p/text()')[0]
            book['star'] = each_book.xpath('tr[@class="item"]/td[@valign="top"]/div[@class="star clearfix"]/span[2]/text()')[0]
            quote = each_book.xpath('tr[@class="item"]/td[@valign="top"]/p[2]/span/text()')
            if quote:
                book['quote'] = quote[0]
            self.post.insert(book)
            book = {}



if __name__ == '__main__':
    c = Douban_book()
    c.setupsession()

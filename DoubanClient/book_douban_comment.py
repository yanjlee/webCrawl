# -*-coding:utf8 -*-
'''
这是一个豆瓣图书top250的爬虫
'''
import requests
import pymongo
from lxml import etree
from multiprocessing.dummy import Pool as Threadings
import json


class DoubanClient():
    def __init__(self):
        header = {
        'Host': 'book.douban.com',
        'Referer': 'https://book.douban.com/top250?icn=index-book250-all',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
        }
        self.session = requests.session()
        self.session.headers.update(header)
        self.connection = pymongo.MongoClient()
    def setupsession(self):
        url = 'https://book.douban.com/subject/1770782/'
        r = self.session.get(url)
        self.session.cookies.update(r.cookies)
        tdb = self.connection.Douban
        self.post = tdb.theCommentOfBook
        return self.getTheBookInfo(r.content)
    def getTheBookInfo(self, content):
        selector = etree.HTML(content)
        print '开始采集书本信息...'
        Book = {}
        Book['title'] = selector.xpath('//*[@id="wrapper"]/h1/span/text()')[0]
        Book['author'] = selector.xpath('//*[@id="info"]/span[1]/a/text()')[0]
        Book['publisher'] = selector.xpath('//*[@id="info"]/span[2]/text()')[0]
        Book['origin_name'] = selector.xpath('//*[@id="info"]/span[3]/text()')[0]
        Book['translator'] = selector.xpath('//*[@id="info"]/span[4]/a/text()')[0]
        Book['time'] = selector.xpath('//*[@id="info"]/span[5]/text()')[0]
        Book['belong'] = selector.xpath('//*[@id="info"]/a/text()')[0]
        Book['ISBN'] = selector.xpath('//*[@id="info"]/span[10]/text()')[0]
        Book['\'' + selector.xpath('//*[@id="content"]/div/div[1]/div[3]/h2[1]/span/text()')[0] + '\''] = \
            selector.xpath('//*[@id="link-report"]/div[1]/div')[0].xpath('string(.)')
        Book['\''+ selector.xpath('//*[@id="content"]/div/div[1]/div[3]/h2[2]/span/text()')[0] + '\''] = \
            selector.xpath('//*[@id="content"]/div/div[1]/div[3]/div[3]/div/div/p/text()')[0]
        self.post.insert(Book)
        #找到链接
        comment_url = selector.xpath('//*[@id="wt_0"]/p/a/@href')[0]

        return self.getComments(comment_url)
    def getComments(self, url):
        selector = etree.HTML(self.session.get(url).content)
        totle_pages = selector.xpath('//*[@id="content"]/div/div[1]/div[2]/a[10]/text()')[0]
        urls = []
        for i in range(int(totle_pages)):
            urls.append('https://book.douban.com/subject/1770782/reviews?start=' + str(i*20))
        #打开多线程
        pool = Threadings(4)
        pool.map(self.getdata, urls)
        print '采集完毕'
        pool.close()
    def getdata(self, url):
        selector = etree.HTML(self.session.get(url))
        comments = selector.xpath('//*[@id="content"]/div/div[1]/div[1]')
        Commts = {}
        for each_comment in comments:
            id = each_comment.xpath('div/div[@class="main review-item"]/@id')[0]
            Commts['title'] = each_comment.xpath('div/div[@class="main review-item"]/div[@class="middle"]/header/h3/a/text()')[0]
            jsonCtx = self.session.get('https://book.douban.com/j/review/'+ str(id) + '/full').content
            js = json.loads(jsonCtx)
            Comments = js['html']
            com = Comments.replace('<br><br>', '').replace('<br>', '')
            Comments['content'] = com
            self.post.insert(Commts)
            Commts = {}

if __name__ == '__main__':
    d = DoubanClient()
    d.setupsession()
# -*- coding:utf8 -*-
'''
16.12.02 修改代码，对于长评论抓取加入线程以提升效率
========分割线=======
爬取电影 《大话西游 月光宝盒》
内容：
电影信息
全部的长影评
之所以选择这部电影，先是先星爷致敬，也是个人非常喜欢的片。
'''

import requests
from lxml import etree
import re
import json
import pymongo
from multiprocessing.dummy import Pool


class theComment():
    def __init__(self):
        object.__init__(self)
        self.header = {
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Host': 'movie.douban.com'
        }
        self.url = 'https://movie.douban.com/subject/1299398/?from=subject-page'  # 月光宝盒的网址
        self.session = requests.session()
        self.session.headers.update(self.header)
        self.connection = pymongo.MongoClient()
    def setupSession(self):
        # 创建链接
        r = self.session.get(self.url)
        # 使用当前cookies
        cookies = r.cookies
        self.session.cookies.update(r.cookies)
        # 初始化mongoDB
        dbName = self.connection.Douban
        self.post = dbName.MovieComment
        return self.modifyForGetMovieInfo(r)


    def modifyForGetMovieInfo(self,r):
        print '开始采集影片信息...'
        movie = {}
        selector = etree.HTML(r.content)
        movieInfo = selector.xpath('//div[@id="info"]')
        for eachInfo in movieInfo:
            movie['\'' + eachInfo.xpath('span[1]/span[@class="pl"]/text()')[0] + '\''] = eachInfo.xpath('span[1]/span[2]/a/text()')[0]
            authors = eachInfo.xpath('span[2]/span[2]/a/text()')
            author = ''
            for each in authors:
                each = each + '/'
                author += each
            movie['\'' + eachInfo.xpath('span[2]/span[1]/text()')[0] + '\''] = author
            actors = re.findall('rel="v:starring">(.*?)</a>', r.content, re.S)
            actor = ''
            for each in actors:
                each = each + '/'
                actor += each
            movie['\'' + eachInfo.xpath('span[3]/span[1]/text()')[0] + '\''] = actor
            movie['\'' +eachInfo.xpath('span[11]/text()')[0] + '\''] = re.search('地区:</span> (.*?)<br/>', r.content, re.S).group(1)
            movie['\'' +eachInfo.xpath('span[12]/text()')[0] + '\''] = re.search('语言:</span>(.*?)<br/>', r.content,re.S).group(1)
            date = eachInfo.xpath('span[@property="v:initialReleaseDate"]/text()')
            onPlayDate = ''
            for each in date:
                each = each + '/'
                onPlayDate += each
            movie['\'' + eachInfo.xpath('span[13]/text()')[0] + '\''] = onPlayDate
            movie['\'' + eachInfo.xpath('span[16]/text()')[0] + '\''] = eachInfo.xpath('span[17]/text()')[0]
            movie['\'' +eachInfo.xpath('span[18]/text()')[0] + '\''] = re.search('又名:</span>(.*?)<br/>', r.content, re.S).group(1)
            self.post.insert(movie)
            movie = {}
        print '影片信息采集结束'
        return self.startGetTheCommentWithThreadings(selector)

    def startGetTheCommentWithThreadings(self,selector):
        print '开始采集评论...'
        #像评论页转跳
        self.new_url = selector.xpath('//*[@id="review_section"]/div[2]/div[6]/a/@href')[0]
        r = self.session.get(self.new_url)
        new_selector = etree.HTML(r.content)
        #采集总页数
        pag_num = new_selector.xpath('//*[@id="content"]/div/div[1]/div[2]/a[10]/text()')[0]
        the_urls = []
        for i in range(int(pag_num)):
            the_urls.append(self.new_url +"start=" + str(i*20))
        #开始多线程
        pool = Pool(4)
        result = Pool(self.getTheComment, the_urls)
        #多线程结束关闭
        result.close()
        pool.close()


    def getTheComment(self, r):
        '''发现每个评论都是对应ID，然后在json里可以提取出全部的内容'''
        comment = {}
        selector = etree.HTML(r.content)
        theMain = selector.xpath('//div[@class="main review-item"]')
        for eachCmt in theMain:
            eachID = eachCmt.xpath('@id')[0]
            eachTitle = eachCmt.xpath('div/header/h3/a/text()')[0].replace('.','')
            #获取json数据
            request_url = 'https://movie.douban.com/j/review/' + eachID + '/full'
            jsContent = self.session.get(request_url).content
            jsDict = json.loads(jsContent)
            Comment = jsDict['html']
            com = Comment.replace('<br><br>', '').replace('<br>', '')
            comment[eachTitle] = com
            self.post.insert(comment)
            comment = {}

        print '采集完毕'





if __name__ == '__main__':
    c = theComment()
    c.setupSession()
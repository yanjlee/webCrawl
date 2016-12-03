# -*- coing:utf8 -*-

'''
完整的豆瓣电影TOP250的抓取
包括每一步的信息，以及长评价
用了4个多线程，仍旧感觉效率不够
'''

from multiprocessing.dummy import Pool as Threadings
import requests
import re
from lxml import etree
import pymongo
import json


class Douban():
    def __init__(self):
        object.__init__(self)
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'Host': 'movie.douban.com'
        }

        self.session = requests.session()
        #设置头
        self.session.headers.update(self.headers)
        self.connection = pymongo.MongoClient()

    def set_up_session(self):
        url = 'http://movie.douban.com/top250'
        r = self.session.get(url)
        cookie = r.cookies
        self.session.cookies.update(cookie)
        # 初始化mongoDB
        dbName = self.connection.Douban
        self.post = dbName.MovieComment
        selector = etree.HTML(r.content)
        total_page = selector.xpath('//*[@id="content"]/div/div[1]/div[2]/a[9]/text()')[0]
        #创建连接池
        urls = []
        for i in range(int(total_page)):
            urls.append('https://movie.douban.com/top250?start='+ str(i*25) + '&filter=')
        #转跳到线程开始
        return self.loading_the_threadings(urls)

    def loading_the_threadings(self, urls):
        pool = Threadings(4)
        pool.map(self.get_all_movies, urls)
        print '采集完毕'
        pool.close()

    def get_all_movies(self, url):
        r = self.session.get(url)
        selector = etree.HTML(r.content)
        input_data = {}
        #创建每一部电影的链接池
        links = []
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            links.append(eachMovie.xpath('div[@class="hd"/a/@href]')[0])
            title = eachMovie.xpath('div[@class="hd"]/a/span/text()')
            full_title = ''
            for each in title:
                full_title += each
            input_data['title'] = full_title
            input_data['movieInfo'] = eachMovie.xpath('div[@class="bd"]/p/text()')[0].replace(' ', '')
            input_data['star'] = \
            eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]
            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')
            if quote:
                input_data['quote'] = quote[0]
            else:
                input_data['quote'] = ''
            self.post_info.insert(input_data)
            input_data = {}
        for link in links:
            com =self.session.get(link)
            self.get_comments(com)

    def get_comments(self, com):
        print '开始采集影片详细信息...'
        movie = {}
        selector = etree.HTML(com.content)
        movieInfo = selector.xpath('//div[@id="info"]')
        for eachInfo in movieInfo:
            movie['\'' + eachInfo.xpath('span[1]/span[@class="pl"]/text()')[0] + '\''] = \
            eachInfo.xpath('span[1]/span[2]/a/text()')[0]
            authors = eachInfo.xpath('span[2]/span[2]/a/text()')
            author = ''
            for each in authors:
                each = each + '/'
                author += each
            movie['\'' + eachInfo.xpath('span[2]/span[1]/text()')[0] + '\''] = author
            actors = re.findall('rel="v:starring">(.*?)</a>', com.content, re.S)
            actor = ''
            for each in actors:
                each = each + '/'
                actor += each
            movie['\'' + eachInfo.xpath('span[3]/span[1]/text()')[0] + '\''] = actor
            movie['\'' + eachInfo.xpath('span[11]/text()')[0] + '\''] = re.search('地区:</span> (.*?)<br/>', com.content,re.S).group(1)
            movie['\'' + eachInfo.xpath('span[12]/text()')[0] + '\''] = re.search('语言:</span>(.*?)<br/>', com.content,re.S).group(1)
            date = eachInfo.xpath('span[@property="v:initialReleaseDate"]/text()')
            onPlayDate = ''
            for each in date:
                each = each + '/'
                onPlayDate += each
            movie['\'' + eachInfo.xpath('span[13]/text()')[0] + '\''] = onPlayDate
            movie['\'' + eachInfo.xpath('span[16]/text()')[0] + '\''] = eachInfo.xpath('span[17]/text()')[0]
            movie['\'' + eachInfo.xpath('span[18]/text()')[0] + '\''] = re.search('又名:</span>(.*?)<br/>', com.content,re.S).group(1)
            self.post.insert(movie)
            movie = {}
        print '影片信息采集结束'
        return self.startGetTheComment(selector)

    def startGetTheComment(self, selector):
        print '开始采集评论...'
        # 向评论页转跳
        self.new_url = selector.xpath('//*[@id="review_section"]/div[2]/div[6]/a/@href')[0]
        r = self.session.get(self.new_url)
        return self.getTheComment(r)
    def getTheComment(self, r):
        '''发现每个评论都是对应ID，然后在json里可以提取出全部的内容'''
        comment = {}
        selector = etree.HTML(r.content)
        theMain = selector.xpath('//div[@class="main review-item"]')
        for eachCmt in theMain:
            eachID = eachCmt.xpath('@id')[0]
            eachTitle = eachCmt.xpath('div/header/h3/a/text()')[0].replace('.', '')
            #获取json数据
            request_url = 'https://movie.douban.com/j/review/' + eachID + '/full'
            jsContent = self.session.get(request_url).content
            jsDict = json.loads(jsContent)
            Comment = jsDict['html']
            com = Comment.replace('<br><br>', '').replace('<br>', '')
            comment[eachTitle] = com
            self.post.insert(comment)
            comment = {}
        #开始翻页
        next_url = selector.xpath('//span[@class="next"]/a/@href')
        if next_url:
            next_link = self.new_url + next_url[0]
            r = self.session.get(next_link)
            return self.do_nextPage(r)

    def do_nextPage(self, r):
        return self.getTheComment(r)

if __name__ == '__main__':
    c = Douban()
    c.set_up_session()


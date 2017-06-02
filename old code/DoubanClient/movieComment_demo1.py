# -*- coding:utf8 -*-
'''
爬取电影 《大话西游 月光宝盒》
内容：
电影信息
全部的长影评
之所以选择这部电影，先是先星爷致敬，也是个人非常喜欢的片。
后续可以延伸到，爬取top250每一部的影评
'''

import requests
from lxml import etree
import re
import json
import pymongo

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
        dbName = self.connection.newDouban
        self.post = dbName.MovieComment
        return self.modifyForGetMovieInfo(r)

    def getMovieInfo(self, r):
        print '开始采集影片信息...'
        movie = {}
        selector = etree.HTML(r.content)
        movieInfo = selector.xpath('//div[@id="info"]')
        for eachInfo in movieInfo:
            t1 = eachInfo.xpath('span[1]/span[@class="pl"]/text()')[0]  #提取 导演
            t2 = eachInfo.xpath('span[1]/span[2]/a/text()')[0]          #提取 刘镇伟
            t3 = eachInfo.xpath('span[2]/span[1]/text()')[0]            #提取 编剧
            t4 = eachInfo.xpath('span[2]/span[2]/a/text()')            #提出两个编剧
            t5 = ''
            for each in t4:
                each = each + '/'
                t5 += each
            t6 = eachInfo.xpath('span[3]/span[1]/text()')[0]             #提出 主演
            t7 = re.findall('rel="v:starring">(.*?)</a>', r.content, re.S)
            t8 = ''
            for each in t7:
                each = each + '/'
                t8 += each
            t9 = eachInfo.xpath('//span[4]/text()')[0]                  #提出 类型
            t10 = eachInfo.xpath('span[@property="v:genre"]/text()')    #提出类型们
            t11 = ''
            for each in t10:
                each = each + '/'
                t11 += each
            t12 = eachInfo.xpath('span[11]/text()')[0]                  #提出地区
            t13 = re.search('地区:</span> (.*?)<br/>', r.content, re.S).group(1)
            t14 = eachInfo.xpath('span[12]/text()')[0]                  #提取 语言
            t15 = re.search('语言:</span>(.*?)<br/>', r.content,re.S).group(1)
            t16 = eachInfo.xpath('span[13]/text()')[0]                  #提取 上映日期
            t17 = eachInfo.xpath('span[@property="v:initialReleaseDate"]/text()')
            t18 = ''
            for each in t17:
                each = each + '/'
                t18 += each
            t19 = eachInfo.xpath('span[16]/text()')[0]                  #提取 片长
            t20 = eachInfo.xpath('span[17]/text()')[0]
            t21 = eachInfo.xpath('span[18]/text()')[0]                  #提取 又名
            t22 = re.search('又名:</span>(.*?)<br/>', r.content, re.S).group(1)
            movie['\''+ t1 + '\''] = t2
            movie['\'' + t3 + '\''] = t5
            movie['\'' + t6 + '\''] = t8
            movie['\'' + t9 + '\''] = t11
            movie['\'' + t12 + '\''] = t13
            movie['\'' + t14 + '\''] = t15
            movie['\'' + t16 + '\''] = t18
            movie['\'' + t19 + '\''] = t20
            movie['\'' + t21 + '\''] = t22
            self.post.insert(movie)
            movie = {}

        print '影片信息采集完毕'
        # return self.startGetTheComment(selector)

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
        return self.startGetTheComment(selector)

    def startGetTheComment(self,selector):
        print '开始采集评论...'
        # selector = etree.HTML(self.r.content)
        #像评论页转跳
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


        #开始翻页
        next_url = selector.xpath('//span[@class="next"]/a/@href')
        if next_url:
            next_link = self.new_url + next_url[0]
            r = self.session.get(next_link)
            return self.do_nextPage(r)

        print '采集完毕'


    def do_nextPage(self, r):
        return self.getTheComment(r)



if __name__ == '__main__':
    c = theComment()
    c.setupSession()

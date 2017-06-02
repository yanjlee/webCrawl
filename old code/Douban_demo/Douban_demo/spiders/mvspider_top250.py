# -*- coding:utf8 -*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from Douban_demo.items import Douban_Movie_top250ITEMS

class Douban_movie_top250(CrawlSpider):
    name = 'Doubanmv250'
    start_urls = ['http://movie.douban.com/top250']
    url = 'http://movie.douban.com/top250'
    def parse(self, response):
        selector = Selector(response)
        Movies = selector.xpath('//div[@class="info"]')
        for eachMovie in Movies:
            item = Douban_Movie_top250ITEMS()
            title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
            full_title = ''
            for each in title:
                full_title += each
                movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()[0].replace(' ', '')
                star = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''

            item['title'] = full_title
            item['star'] = star
            item['movieInfo'] = movieInfo
            item['quote'] =quote

            yield item

        nextLink = selector.xpath('//span[@class="next"]/a/@href').extract()
        if nextLink:
            nextLink = nextLink[0]
            print nextLink
            yield Request(self.url + nextLink, callback= self.parse)
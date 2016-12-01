# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class DoubanDemoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Douban_Movie_top250ITEMS(Item):
    title = Field()
    star =Field()
    movieInfo = Field()
    quote = Field()
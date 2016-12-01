# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
# from items import Douban_Movie_top250ITEMS
import pymongo

class DoubandemoPipeline(object):
    def process_item(self, item, spider):
        return item


class Douban_Movie_top250_pipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient()
        tdb = client[dbName]
        self.post = tdb[settings['MONGODB_DOCNAME']]
        '''在这里面，可以看出， ‘.’ 来调取不可用，得换成[]来调用'''

    def process_item(self, item, spider):
        movie = dict(item)
        print movie
        self.post.insert(movie)
        # test = {'name': 'wangjiawei', 'lover': 'taozi'}
        # self.post.insert(test)
        return item

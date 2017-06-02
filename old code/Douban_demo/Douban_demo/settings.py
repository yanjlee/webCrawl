# -*- coding: utf-8 -*-

# Scrapy settings for Douban_demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Douban_demo'

SPIDER_MODULES = ['Douban_demo.spiders']
NEWSPIDER_MODULE = 'Douban_demo.spiders'


USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'



#定义一个数据库
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'Douban'
MONGODB_DOCNAME = 'top_movie'



COOKIES_ENABLED = True


ITEM_PIPELINES = {
   'Douban_demo.pipelines.Douban_Movie_top250_pipeline': 100,
}



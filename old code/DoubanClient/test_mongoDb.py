# -*-coding:utf8 -*-
import pymongo

connection = pymongo.MongoClient()
tdb = connection.testDemo  #创建数据库
post_info = tdb.test    #创建collection

jiawei = {'name': 'wangjiawei', 'age': '25', 'skill': 'Python'}
taozi= {'name': 'wanshengtao', 'age': '21', 'skill': 'java', 'other': 'shi is my wife'}

post_info.insert(jiawei)
post_info.insert(taozi)
print 'it\'s done'
# coding=utf8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
'''DB_URI需要添加对应的数据库'''
DB_URI = 'mysql://root:454647@localhost:3306/testFlask'

eng = create_engine(DB_URI)
Base = declarative_base()
#这就创建好一个mysql的orm了


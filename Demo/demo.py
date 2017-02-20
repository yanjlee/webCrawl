# coding=utf8
'''这是一个爬虫脚本,model和ua从别的类来调用'''
from userAgent import user_agent_list
from sqlalchemy.orm import sessionmaker
from sqlEngine import Base, eng
from models import User
import requests
import random


class Demo():
    def __init__(self):
        '''初始化内容'''
        self.headers = {
            'host': '主机地址',
            'User-Agent': random.choice(user_agent_list)
        }
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def demo(self):
        '''存放工作函数'''
        pass


    def dealWithModels(self):
        '''数据内容,即可以放缓存中清洗,也可以直接放入数据库'''
        Base.metadata.drop_all(bind=eng)
        Base.metadata.create_all(bind=eng)

        Session = sessionmaker(bind=eng)
        session = Session()
        #录入数据测试用.
        session.add_all([User(name=username) for username in ('wangjiawei', 'wanshengtao')])

        session.commit()

if __name__ == '__main__':
    c = Demo()
    #调用函数
    # c.dealWithModels()
    # c.demo()
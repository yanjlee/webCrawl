# coding=utf-8
'''初始化模型'''
from flask_sqlalchemy import SQLAlchemy
from main import app


db = SQLAlchemy(app)


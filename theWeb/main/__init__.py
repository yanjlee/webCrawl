# coding=utf-8

from flask import Flask
import flask_login
app = Flask(__name__)

#配置
app.secret_key = 'do IT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:454647@localhost:3306/testFlask?charset=utf8'

login_manager = flask_login.LoginManager()
from utils import *

#添加路由
from routs import *
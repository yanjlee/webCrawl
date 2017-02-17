# coding=utf-8
from . import db
import flask_login

class Visitor(flask_login.UserMixin, db.Model):
    '''在UserMixin这里面有一些用户相关的属性,不然的话会提示Flask里没有 is_active'''
    __tablename__ = 'visitors'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(500), nullable=False)
    load_count = db.Column(db.Integer, default=0)
    load_ip = db.Column(db.String(128), default='unknow')

    def __init__(self, id=None, name=None, load_count=None, load_ip=None):
        self.id = id
        self.name = name
        self.load_count = load_count
        self.load_ip = load_ip

    def __repr__(self):
        return '<id= %s>' %id

db.create_all()
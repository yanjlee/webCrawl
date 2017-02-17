# coding=utf-8

import flask_login
from . import app, login_manager
from models.visitors import Visitor
from flask import request
from models import db
#这里有个init,说明是反正是某种app的初始化
login_manager.init_app(app)

@flask_login.user_logged_in.connect_via(app)
def _track_logins(sender, user, **extra):
    user.load_count += 1
    user.load_ip = request.remote_addr
    db.session.add(user)
    db.session.commit()
'''
    Sent when a user is logged in. In addition to the app (which is thesender),
    it is passed `user`, which is the user being logged in.
 '''



@login_manager.user_loader
def user_loader(id):
    visitor = Visitor.query.filter_by(id=id).first()
    return visitor


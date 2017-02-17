# coding=utf-8

from flask import request, redirect, url_for
from main import app
from models.visitors import Visitor
from models import db
import flask_login


@app.route('/')
def hello_page():
    return '''
    <html>
        <head>
            <title>welcome page</title>
        </head>
        <body>
            <h1>hello welcome to my website</h1>
        </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <html>
                <head>
                    <title>welcome page</title>
                </head>
                <body>
                    <form action='login' method='POST'>
                        <input type='text' name='name' id='name' placeholder='name'></input>
                        <input type='password' name='pw' id='pw' placeholder='password'></input>
                        <input type='submit' name='submit'></input>
                    </form>
                </body>
            </html>
        '''
    name = request.form.get('name')
    if request.form.get('pw') == '123':
        visitor = Visitor.query.filter_by(name=name).first()
        if not visitor:
            visitor = Visitor(name=name)
            db.session.add(visitor)
            db.session.commit()
        flask_login.login_user(visitor)
        return redirect(url_for('protected'))
    return 'Bad Login'

@app.route('/protected')
@flask_login.login_required
def protected():
    visitor = flask_login.current_user
    return '''
            <html>
                <head>
                    <title>welcome page</title>
                </head>
                <body>
                    <h1>Loggin in as:{}|loggin_count:{}|loggin_ip{}</h1>
                </body>
            </html>
        '''.format(visitor.name, visitor.load_count, visitor.load_ip)

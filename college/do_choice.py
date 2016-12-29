# -*- coding:utf8 -*-


import re
import MySQLdb

def choice():
    text = open('demo27').read()
    name = re.findall('\'(.*?)\'', text, re.S)[0]
    content = re.findall('~(.*?);', text, re.S)[0]
    print content
    sc = re.findall('(.*?)\n', content, re.S)
    u = []
    for i in sc:
        u.append(i)
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='454647',
        db='college_info',
        charset="utf8"
    )
    cur = conn.cursor()

    for i in u:
        SQL = 'insert into 重点中学名单 (学校名称,城市,省份,备注)values(\'' + str(i) +'\',\'' + name + '\',\'新疆\',\'新疆自治区区级示范高中\')'
        print  SQL
        cur.execute(SQL)
    conn.commit()
choice()
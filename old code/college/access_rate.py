# -*-coding:utf8-*-

import re
import MySQLdb

def get():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='454647',
        db='college_info',
        charset="utf8"
    )
    cur = conn.cursor()
    SQL_d = 'create table 逐年录取率(id int auto_increment primary key,时间 nvarchar(10),参考人数 nvarchar(10)' \
            ',录取人数 nvarchar(10),录取率 nvarchar(10));'
    cur.execute(SQL_d)

    text = open('access_rate').read()
    # each_year = re.findall('\n(\d{4})', text, re.S)
    # each_totle = re.findall('\t(\d{3,4}),', text, re.S)
    # each_ac_num = re.findall(',\t(\d{2,3}).', text, re.S)
    # each_rate = re.findall('.\t()%/', text, re.S)
    content = re.findall('\n(.*?)/', text, re.S)
    for each in content:
        year = re.findall('(\d{4})\t', each, re.S)[0]
        total = re.findall('\t(.*?),', each, re.S)[0]
        num = re.findall('(\d{2,3}|\d\d.\d);', each, re.S)[0]
        rate = re.findall('(\d{1,2}|\d\d.\d)%', each, re.S)[0]
        sql = 'insert into 逐年录取率(时间,参考人数,录取人数,录取率)values(\'%s\',\'%s\',\'%s\',\'%s\')'%(year, total, num, rate)
        cur.execute(sql)
    conn.commit()
    conn.close()


get()
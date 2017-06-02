# -*- coding:utf8 -*-

import re
import MySQLdb

def run():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='454647',
        db='college_info',
        charset="utf8"
    )
    cur = conn.cursor()

    text = open('a_1.csv')
    for i in range(92):
        t = text.readline()
        name = re.findall(',(.*?),\d{4}', t, re.S)
        if name:
            sql = 'insert into college_list(所在省市,院校名称,办学性质,重点学科,院士,博士点,硕士点,通讯地址) select ' \
                  '所在省市,院校名称,办学类型,重点学科,院士,博士点,硕士点,通讯地址 from new_全国高校基本数据 where 院校名称=\'' + name[0] +'\';'
            cur.execute(sql)
            conn.commit()
        else:
            print 't', t
    conn.close()
run()
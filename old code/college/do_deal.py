# -*-coding:utf8-*-

import MySQLdb
import sys
reload(sys)


sys.setdefaultencoding('utf-8')

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
    sql_safe = 'set sql_safe_updates=0'
    cur.execute(sql_safe)
    #修改表的一级学科编码
    sql = 'select * from course_data_1 group by 一级专业编码'
    cur.execute(sql)
    text = cur.fetchall()
    n = 1
    for each in text:
        print each[0], each[1], each[2], each[3], each[4], each[5], each[6], each[7], each[8]
        if n < 10:
            yiji = str(each[2]) + str(0) + str(n)
        elif n > 9:
            yiji = str(each[2]) + str(n)
        print yiji
        n += 1
        sql_1 = 'update course_data_1 set 一级专业编码=\'' + yiji + '\'' \
                 ' where 一级学科=\'' + each[3]  +'\';'
        # print sql_1
        cur.execute(sql_1)
        conn.commit()

    #
    sql = 'select * from course_data_1 group by 一级学科 order by id'
    cur.execute(sql)
    text = cur.fetchall()
    list = []

    for i in text:
        list.append(i[3])

    for each in list:
        print each
        sql_2 = 'select * from course_data_1 where 一级学科=\'' + each +'\' order by id'
        cur.execute(sql_2)
        text_2 = cur.fetchall()
        n = 1
        for t in text_2:
            print t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8]
            if n < 10:
                print n
                yiji = str(t[4]) + str(0) + str(n)
                sql_3 = 'update course_data_1 set 二级专业编码=\'' + yiji + '\' where 一级学科=\'' + t[3] + '\' and 二级学科=\'' \
                        + t[5] + '\' and ﻿本专科=\'' + t[1]+ '\';'
                cur.execute(sql_3)
                conn.commit()
            elif n > 9:
                yiji = str(t[4]) + str(n)
                sql_3 = 'update course_data_1 set 二级专业编码=\'' + yiji + '\' where 一级学科=\'' + t[3] + '\' and 二级学科=\'' \
                        + t[5] + '\' and ﻿本专科=\'' + t[1] + '\';'
                cur.execute(sql_3)
                conn.commit()

            # print yiji
            n += 1
            # print sql_3


    sql = 'select * from course_data_1 group by 二级学科 order by id'
    cur.execute(sql)
    text = cur.fetchall()
    list = []

    for i in text:
        list.append(i[3])

    for each in list:
        # print each
        sql_2 = 'select * from course_data_1 where 一级学科=\'' + each +'\' order by id;'
        cur.execute(sql_2)
        text_2 = cur.fetchall()
        n = 1
        for t in text_2:
            print t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8]
            if n < 10:
                yiji = str(t[6]) + str(0) + str(n)
                sql_4 = 'update course_data_1 set 三级学科编码=\'' + yiji + '\' where 一级学科=\'' + t[3] + '\' and 二级学科=\'' \
                        + t[5] + '\' and 三级学科=\'' + t[7] + '\' and ﻿本专科=\'' + t[1] + '\';'
                cur.execute(sql_4)
                conn.commit()
            elif n > 9:
                yiji = str(t[6]) + str(n)
                sql_4 = 'update course_data_1 set 三级学科编码=\'' + yiji + '\' where 一级学科=\'' + t[3] + '\' and 二级学科=\'' \
                        + t[5] + '\' and 三级学科=\'' + t[7] + '\' and ﻿本专科=\'' + t[1] + '\';'
                cur.execute(sql_4)
                conn.commit()
            # print yiji
            n += 1






    conn.close()
run()
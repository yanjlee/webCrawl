# -*- coding:utf8 -*-

import MySQLdb
import sys
reload(sys)

sys.setdefaultencoding('utf-8')


def test():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='454647',
        db='college_data',
        charset="utf8"
    )
    cur = conn.cursor()
    # safe = 'set sql_safe_updates=0'
    # cur.execute(safe)
    # sql = 'select * from temp_0113'
    # cur.execute(sql)
    # total = cur.fetchall()
    # # total = cur.fetchmany(150)
    # n = 1
    # for i in total:
    #     if i:
    #         n += 1
    #         name = i[0]
    #         course = i[1]
    #         type = i[2]
    #         print n, name, course, type
    #         sql_2 = 'select 专业名称 from college_course_line where 院校名称=\'' + name +'\' and 专业名称 like \'%'\
    #                 + course +'%\' and 考生类别=\''+ type +'\';'
    #         # print sql_2
    #         cur.execute(sql_2)
    #         s_1 = cur.fetchone()
    #         if s_1:
    #             sql_3 = 'update college_course_line set 专业名称=\''+ course + '\' where 院校名称=\'' + name +'\'and 专业名称' \
    #                                                                 ' like \'%'+ course + '%\' and 考生类别=\''+ type +'\''
    #             cur.execute(sql_3)
    #             conn.commit()
    #             # print sql_3
    #         else: continue

    '''
    开始处理，添加到表
    '''
    year = [2011, 2012, 2013, 2014, 2015]
    safe = 'set sql_safe_updates=0'
    cur.execute(safe)
    sql = 'select * from temp_p'
    SQL= 'update temp_p set 2011年录取分数= (select 最低分 from temp_course_use where ' \
         '院校名称=\'清华大学\' and 专业名称=\'材料科学与工程\' and 年份=2011 and 省份=\'北京\')where院校名称=\'清华大学\' ' \
         'and 专业名称=\'材料科学与工程\';'
    cur.execute(sql)
    total = cur.fetchall()
    n = 0
    for i in total:
        for y in year:
            if i:
                n += 1
                name = i[3]
                course = i[4]
                type = i[5]
                print n, y, name, course, type
                t = name+course+' 北京'+type
                # print t
                SQL = 'update temp_p set ' + str(y)+'年录取分数= (select 平均分 from temp_c where temp=\''+ t+'\'and' \
                ' 年份=' + str(y) + ' )where 院校名称=\''+ name+ '\'and 专业名称=\'' + course + '\'and 科类=\'' + type + '\';'
                # print SQL

                cur.execute(SQL)
                conn.commit()
    conn.close()

test()
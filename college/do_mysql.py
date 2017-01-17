# -*- coding:utf8 -*-

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
        db='college_data',
        charset="utf8"
    )
    cur = conn.cursor()
    safe = 'set sql_safe_updates=0'
    cur.execute(safe)
    '''
    两个表的链接
    sql_q = 'select * from data_course;'
    cur.execute(sql_q)
    text = cur.fetchall()
    n = 1
    for each in text:
        school = each[5]
        course = each[6]
        type = each[7]
        if type == '文史':
            q = 'select 平均分 from data_c_line2 where temp like \''+ school + '%' + course + '%2015四川' + type + '\''
            cur.execute(q)
            cx = cur.fetchone()
            if cx:
                # print cx[0]
                sql_u = 'update data_course set 2017年分数预测=(\'' + cx[0] +'\')' \
                        'where 院校名称=\'' + school + '\' and 专业名称=\'' + course +'\' and 科类=\'' + type +'\';'
                cur.execute(sql_u)
                conn.commit()
                # print sql_u
                print n, school, course, type
            n += 1
    conn.close()
    '''
    #添加专科
    '''
    sql_1 = 'select 院校名称 from rank_zhuanke'
    cur.execute(sql_1)
    total = cur.fetchall()
    n = 1
    for each in total:
        name =  each[0]
        if n in range(1, 101):
            sqld_1 = 'update data_course set 2017年分数预测=448 where 院校名称=\'' + name +'\'and 科类=\'文史\';'
            sqld_2 = 'update data_course set 2017年分数预测=412 where 院校名称=\'' + name + '\'and 科类=\'理工\';'
            cur.execute(sqld_1)
            cur.execute(sqld_2)
            conn.commit()
        if n in range(101, 501):
            sqld_1 = 'update data_course set 2017年分数预测=348 where 院校名称=\'' + name +'\'and 科类=\'文史\';'
            sqld_2 = 'update data_course set 2017年分数预测=312 where 院校名称=\'' + name + '\'and 科类=\'理工\';'
            cur.execute(sqld_1)
            cur.execute(sqld_2)
            conn.commit()
        if n in range(501, 1001):
            sqld_1 = 'update data_course set 2017年分数预测=248 where 院校名称=\'' + name +'\'and 科类=\'文史\';'
            sqld_2 = 'update data_course set 2017年分数预测=212 where 院校名称=\'' + name + '\'and 科类=\'理工\';'
            cur.execute(sqld_1)
            cur.execute(sqld_2)
            conn.commit()
        if n in range(1001, len(total)):
            sqld_1 = 'update data_course set 2017年分数预测=200 where 院校名称=\'' + name +'\'and 科类=\'文史\';'
            sqld_2 = 'update data_course set 2017年分数预测=200 where 院校名称=\'' + name + '\'and 科类=\'理工\';'
            cur.execute(sqld_1)
            cur.execute(sqld_2)
            conn.commit()
        print n
        n += 1
    conn.close()
    '''
    #录入专科排名
    '''
    sql_1 = 'select 排名,院校名称 from rank_zhuanke'
    cur.execute(sql_1)
    total = cur.fetchall()
    n = 1
    for each in total:
        rank = each[0]
        name = each[1]
        print n, rank, name
        sql = 'update data_course_final2 set 名次=' + rank + ' where 院校名称=\'' + name + '\';'
        cur.execute(sql)
        conn.commit()
    conn.close()
    '''
    #修改省份
    province = {
        '10': '北京', '11': '上海', '26': '广东', '12': '天津', '13': '重庆', '21': '湖北', '31': '四川',
        '14': '河北', '15': '河南', '16': '山东', '17': '山西', '19': '江苏', '18': '陕西', '23': '浙江',
        '24': '江西', '27': '广西', '20': '湖南', '40': '辽宁', '22': '安徽', '25': '福建', '30': '贵州',
        '35': '甘肃', '39': '吉林', '28': '海南', '29': '云南', '33': '新疆', '36': '宁夏', '32': '西藏',
        '34': '青海', '37': '内蒙古', '38': '黑龙江', '41': '香港', '42': '澳门'
    }
    for p in province.keys():
        sql = 'update data_course_final2 set 省编号=' + p + ' where 省市=\'' + province[p] + '\';'
        cur.execute(sql)
        conn.commit()
        print p
    conn.close()


run()
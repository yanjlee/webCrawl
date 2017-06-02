# -*- coding:utf8 -*-

import MySQLdb
import sys
reload(sys)

sys.setdefaultencoding('utf-8')
def run():
    province = {
        '10003': '北京', '10000': '上海', '10011': '广东', '10006': '天津', '10028': '重庆', '10021': '湖北', '10005': '四川',
        '10016': '河北', '10017': '河南', '10009': '山东', '10010': '山西', '10014': '江苏', '10029': '陕西', '10018': '浙江',
        '10015': '江西', '10012': '广西', '10022': '湖南', '10027': '辽宁', '10008': '安徽', '10024': '福建', '10026': '贵州',
        '10023': '甘肃', '10004': '吉林', '10019': '海南', '10001': '云南', '10013': '新疆', '10007': '宁夏', '10025': '西藏',
        '10030': '青海', '10002': '内蒙古', '10031': '黑龙江'
    }
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='454647',
        db='college_data',
        charset="utf8"
    )
    cur = conn.cursor()
    #处理建表，录入数据
    '''
    for p in province.values():
        print p
        sql_1 = 'create table data_' + p +'(省编号 nvarchar(10),省市 nvarchar(10),学校编号 nvarchar(10),本专科 nvarchar(10),' \
                '排名 nvarchar(50),院校名称 nvarchar(100),专业名称 nvarchar(100),科类 nvarchar(50),备注 nvarchar(500),' \
                '编号 nvarchar(50),权重 nvarchar(50),就业方向 nvarchar(500),对应性格类型 nvarchar(50),性别限制 nvarchar(50),' \
                '色盲色弱要求 nvarchar(50),身体情况要求 nvarchar(50),2017年分数预测 nvarchar(50));'
        # print sql_1
        # break
        cur.execute(sql_1)
        conn.commit()
        sql_2 = 'LOAD DATA INFILE \'/var/lib/mysql-files/final_data.csv\' INTO TABLE data_' + p +' CHARACTER SET utf8 FIELDS' \
                ' TERMINATED BY \',\' ENCLOSED BY \'"\';'
        cur.execute(sql_2)
        conn.commit()
    conn.close()
    '''
    #删除第一行
    '''
    sql_safe = 'set sql_safe_updates=0'
    cur.execute(sql_safe)
    for p in province.values():
        sql_1 = 'delete from data_' + p + ' where 省市=\'省市\';'
        # print sql_1
        cur.execute(sql_1)
        conn.commit()
    conn.close()
    '''
    #导入学校id，省份
    '''
    sql_safe = 'set sql_safe_updates=0'
    cur.execute(sql_safe)
    for p in province.values():
        print p
        sql_1 = 'create table import_data_' + p +'(select a.省编号,b.所在省市 as 省市,b.编号 as 学校编号,a.本专科,a.排名,' \
                 'a.院校名称,a.专业名称,a.科类,a.备注,a.编号,a.权重,a.就业方向,a.对应性格类型,a.性别限制,a.色盲色弱要求,a.身体情况要求,' \
                 'a.2017年分数预测 from data_' + p + ' a left join college_list b on a.院校名称=b.院校名称);'
        cur.execute(sql_1)
        conn.commit()
        sql_2 = 'delete from import_data_' + p + ' where 省市 is null'
        cur.execute(sql_2)
        sql_3 = 'drop table data_' + p
        cur.execute(sql_3)
        conn.commit()
    conn.close()
    '''
    #修正专业 会计->会计类
    '''
    sql_safe = 'set sql_safe_updates=0'
    cur.execute(sql_safe)
    for p in province.values():
        print p
        sql_1 = 'update import_data_' + p + ' set 专业名称=\'会计学\' where 专业名称 like \'%会计%\';'
        # print sql_1
        cur.execute(sql_1)
        conn.commit()
    conn.close()
    '''
    #录入数据
    safe = 'set sql_safe_updates=0'
    cur.execute(safe)
    nn = 1
    n = 1
    for p in province.values():
        # sql_deal = 'alter table import_data_' + p + ' add column temp nvarchar(100);'
        # sql_deal_2 = 'update import_data_' + p + ' set temp=concat(院校名称,专业名称,省市,科类);'
        # sql_deal_3 = 'create index z' + str(n) + ' on import_data_' + p + '(temp);'
        # cur.execute(sql_deal)
        # conn.commit()
        # print sql_deal_2
        # cur.execute(sql_deal_2)
        # conn.commit()
        # cur.execute(sql_deal_3)
        # conn.commit()
        sql = 'select * from import_data_' + p
        SQL = 'update temp_p set 2017年分数预测= (select 最低分 from temp_course_use where ' \
              '院校名称=\'清华大学\' and 专业名称=\'材料科学与工程\' and 年份=2011 and 省份=\'北京\')where院校名称=\'清华大学\' ' \
              'and 专业名称=\'材料科学与工程\';'
        cur.execute(sql)
        total = cur.fetchall()
        for i in total:
            name = i[5]
            course = i[6]
            type = i[7]
            print n, p, ':', nn,  name, course, type
            t = name + course + ' ' + p + type
            # print t
            SQL = 'update import_data_' + p + ' set 2017年分数预测= (select 平均分 from temp_c where temp=\'' + t + '\' ' \
                  'and 年份=2015)where 院校名称=\'' + name + '\'and 专业名称=\'' + course + '\'and 科类=\'' + type + '\';'
            cur.execute(SQL)
            conn.commit()
            nn += 1
        n += 1
        # sql_drop = 'drop index z' + str(n) + 'on import_data_' + p

run()
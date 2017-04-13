# coding=utf8

import time, random, json, requests, os
from hdfs3 import HDFileSystem
global HDFS
HDFS = HDFileSystem(host='192.168.100.178', port=8020)
city = {'山西\x01长治': '228', '河北\x01承德': '145', '西藏\x01林芝': '656', '西藏\x01日喀则': '516', '辽宁\x01葫芦岛': '225',
        '湖北\x01仙桃': '42', '安徽\x01淮北': '183', '山东\x01淄博': '81', '内蒙古\x01锡林郭勒盟': '19', '黑龙江\x01绥化': '324',
        '辽宁\x01抚顺': '222', '山西\x01临汾': '232', '云南\x01昭通': '335', '黑龙江\x01牡丹江': '322', '贵州\x01黔西南': '588',
        '新疆\x01巴音郭楞': '499', '新疆\x01昌吉': '311', '贵州\x01贵阳': '2', '甘肃\x01嘉峪关': '286',
        '新疆\x01克孜勒苏柯尔克孜': '653', '甘肃\x01天水': '308', '山东\x01潍坊': '80', '湖北\x01荆州': '31',
        '湖北\x01襄樊': '32', '广东\x01梅州': '211', '湖南\x01衡阳': '45', '甘肃\x01酒泉': '284',
        '甘肃\x01金昌': '343', '天津\x01天津': '164', '广东\x01珠海': '200', '四川\x01南充': '104',
        '广东\x01揭阳': '205', '广东\x01韶关': '201', '河北\x01保定': '259', '山东\x01泰安': '353',
        '广东\x01东莞': '133', '云南\x01昆明': '117', '福建\x01漳州': '56', '河南\x01信阳': '373',
        '新疆\x01塔城': '563', '湖北\x01黄石': '30', '新疆\x01哈密': '312', '湖北\x01十堰': '36', '山东\x01枣庄': '85',
        '河南\x01平顶山': '266', '福建\x01南平': '253', '宁夏\x01石嘴山': '472', '甘肃\x01白银': '309', '辽宁\x01营口': '221',
        '陕西\x01宝鸡': '273', '广西\x01贵港': '93', '江苏\x01徐州': '161', '浙江\x01舟山': '306', '新疆\x01伊犁': '520',
        '内蒙古\x01巴彦淖尔': '15', '山西\x01运城': '233', '广西\x01梧州': '132', '台湾\x01台湾': '931', '湖北\x01孝感': '41',
        '江苏\x01南京': '125', '广东\x01清远': '208', '山东\x01临沂': '79', '河北\x01张家口': '144', '陕西\x01延安': '401',
        '黑龙江\x01齐齐哈尔': '319', '安徽\x01合肥': '189', '湖南\x01张家界': '226', '吉林\x01吉林': '270',
        '海南\x01万宁': '241', '陕西\x01铜川': '271', '广东\x01佛山': '196', '新疆\x01喀什': '384', '广西\x01北海': '128',
        '贵州\x01铜仁': '422', '甘肃\x01陇南': '344', '贵州\x01遵义': '59', '四川\x01自贡': '111', '陕西\x01渭南': '275',
        '辽宁\x01盘锦': '151', '澳门\x01澳门': '664', '贵州\x01六盘水': '4', '河南\x01商丘': '376', '河南\x01驻马店': '371',
        '辽宁\x01鞍山': '215', '四川\x01攀枝花': '112', '湖南\x01湘西': '65', '安徽\x01亳州': '391', '陕西\x01汉中': '276',
        '云南\x01曲靖': '339', '吉林\x01松原': '194', '广西\x01玉林': '118', '江西\x01吉安': '115', '山东\x01烟台': '78',
        '云南\x01红河': '337', '山东\x01聊城': '83', '山东\x01威海': '88', '四川\x01成都': '97', '湖南\x01邵阳': '405',
        '云南\x01楚雄': '124', '广东\x01中山': '207', '西藏\x01拉萨': '466', '河南\x01鹤壁': '374', '广东\x01广州': '95',
        '新疆\x01乌鲁木齐': '467', '广西\x01钦州': '129', '上海\x01上海': '57', '广东\x01河源': '210', '西藏\x01那曲': '655',
        '江苏\x01宿迁': '172', '浙江\x01台州': '287', '安徽\x01池州': '175', '广西\x01柳州': '89', '内蒙古\x01呼和浩特': '20',
        '广东\x01江门': '198', '贵州\x01毕节': '426', '四川\x01广安': '108', '黑龙江\x01鹤岗': '301', '四川\x01凉山': '479',
        '江苏\x01泰州': '159', '贵州\x01黔南': '3', '云南\x01丽江': '342', '湖南\x01长沙': '43', '甘肃\x01临夏': '346',
        '安徽\x01六安': '181', '辽宁\x01辽阳': '224', '北京\x01北京': '514', '云南\x01临沧': '350', '黑龙江\x01双鸭山': '359',
        '河北\x01唐山': '261', '江西\x01九江': '6', '广东\x01潮州': '204', '海南\x01琼海': '242', '河南\x01安阳': '370',
        '江苏\x01淮安': '157', '浙江\x01嘉兴': '304', '青海\x01西宁': '139', '陕西\x01安康': '272', '安徽\x01巢湖': '177',
        '福建\x01莆田': '51', '江西\x01南昌': '5', '吉林\x01通化': '407', '黑龙江\x01大兴安岭': '297', '安徽\x01铜陵': '173',
        '江苏\x01镇江': '169', '湖南\x01郴州': '49', '云南\x01大理': '334', '四川\x01广元': '99', '陕西\x01商洛': '274',
        '云南\x01思茅': '662', '内蒙古\x01乌兰察布': '331', '陕西\x01西安': '165', '江西\x01景德镇': '137',
        '河南\x01濮阳': '380', '广东\x01肇庆': '209', '广西\x01南宁': '90', '河北\x01沧州': '148', '新疆\x01伊犁哈萨克': '660',
        '广东\x01云浮': '195', '山东\x01滨州': '76', '重庆\x01重庆': '11', '云南\x01文山': '437', '辽宁\x01丹东': '219',
        '辽宁\x01大连': '29', '江西\x01新余': '246', '河南\x01焦作': '265', '湖北\x01荆门': '34', '福建\x01宁德': '87',
        '四川\x01乐山': '107', '黑龙江\x01大庆': '153', '江西\x01抚州': '8', '湖南\x01娄底': '66', '陕西\x01榆林': '278',
        '四川\x01眉山': '291', '内蒙古\x01鄂尔多斯': '14', '宁夏\x01吴忠': '395', '新疆\x01阿勒泰': '383', '辽宁\x01阜新': '223',
        '陕西\x01咸阳': '277', '山西\x01朔州': '235', '吉林\x01延边': '525', '广东\x01阳江': '202', '新疆\x01吐鲁番': '310',
        '吉林\x01四平': '155', '安徽\x01黄山': '174', '辽宁\x01铁岭': '218', '四川\x01遂宁': '100', '河南\x01郑州': '168',
        '河北\x01石家庄': '141', '宁夏\x01中卫': '480', '香港\x01香港': '663', '山东\x01莱芜': '356', '新疆\x01石河子': '280',
        '河南\x01周口': '375', '河北\x01邯郸': '292', '青海\x01玉树': '659', '河南\x01三门峡': '381', '内蒙古\x01兴安盟': '333',
        '山西\x01太原': '231', '甘肃\x01武威': '283', '福建\x01三明': '52', '河北\x01秦皇岛': '146', '山西\x01忻州': '229',
        '辽宁\x01本溪': '220', '新疆\x01克拉玛依': '317', '山东\x01济宁': '352', '河南\x01南阳': '262', '广东\x01深圳': '94',
        '江苏\x01苏州': '126', '海南\x01儋州': '244', '山西\x01晋中': '230', '四川\x01巴中': '101', '山西\x01大同': '227',
        '云南\x01保山': '438', '宁夏\x01银川': '140', '四川\x01宜宾': '96', '山西\x01阳泉': '236', '广东\x01汕尾': '213',
        '福建\x01龙岩': '53', '吉林\x01长春': '154', '河北\x01衡水': '143', '广西\x01百色': '131', '安徽\x01阜阳': '184',
        '广东\x01湛江': '197', '湖北\x01潜江': '74', '湖北\x01恩施': '38', '四川\x01雅安': '114', '海南\x01东方': '456',
        '河南\x01新乡': '263', '内蒙古\x01阿拉善盟': '17', '广东\x01茂名': '203', '浙江\x01宁波': '289', '内蒙古\x01乌海': '16',
        '浙江\x01湖州': '305', '河南\x01开封': '264', '四川\x01达州': '113', '广西\x01防城港': '130', '青海\x01海东': '652',
        '湖南\x01怀化': '67', '甘肃\x01兰州': '166', '安徽\x01马鞍山': '185', '湖北\x01天门': '73', '江苏\x01南通': '163',
        '山东\x01济南': '1', '新疆\x01和田': '386', '甘肃\x01庆阳': '281', '江苏\x01盐城': '160', '云南\x01玉溪': '123',
        '内蒙古\x01通辽': '22', '江西\x01赣州': '10', '青海\x01海西': '608', '江苏\x01连云港': '156', '广西\x01河池': '119',
        '广东\x01惠州': '199', '河南\x01许昌': '268', '四川\x01内江': '102', '湖南\x01岳阳': '44', '江苏\x01扬州': '158',
        '山东\x01日照': '366', '四川\x01绵阳': '98', '江西\x01鹰潭': '7', '福建\x01厦门': '54', '河北\x01廊坊': '147',
        '河北\x01邢台': '293', '湖北\x01武汉': '28', '海南\x01五指山': '582', '广西\x01来宾': '506', '安徽\x01淮南': '178',
        '广西\x01贺州': '92', '山西\x01吕梁': '237', '江苏\x01常州': '162', '新疆\x01博尔塔拉': '318', '新疆\x01五家渠': '661',
        '广东\x01汕头': '212', '四川\x01德阳': '106', '内蒙古\x01包头': '13', '内蒙古\x01赤峰': '21', '贵州\x01黔东南': '61',
        '浙江\x01衢州': '288', '浙江\x01绍兴': '303', '辽宁\x01朝阳': '216', '湖北\x01宜昌': '35', '河南\x01洛阳': '378',
        '黑龙江\x01黑河': '300', '福建\x01福州': '50', '内蒙古\x01呼伦贝尔': '25', '浙江\x01杭州': '138', '江西\x01萍乡': '136',
        '山东\x01菏泽': '84', '四川\x01阿坝': '457', '浙江\x01丽水': '134', '安徽\x01宣城': '176', '吉林\x01白山': '408',
        '甘肃\x01定西': '282', '湖南\x01常德': '68', '吉林\x01辽源': '191', '河南\x01漯河': '379', '甘肃\x01平凉': '307',
        '四川\x01资阳': '109', '黑龙江\x01伊春': '295', '安徽\x01滁州': '182', '安徽\x01安庆': '186', '山东\x01青岛': '77',
        '江西\x01宜春': '256', '湖北\x01随州': '37', '海南\x01三亚': '243', '浙江\x01温州': '149', '宁夏\x01固原': '396',
        '广西\x01桂林': '91', '四川\x01泸州': '103', '安徽\x01宿州': '179', '辽宁\x01沈阳': '150', '黑龙江\x01七台河': '302',
        '湖南\x01株洲': '46', '四川\x01甘孜': '417', '辽宁\x01锦州': '217', '贵州\x01安顺': '424', '福建\x01泉州': '55',
        '甘肃\x01张掖': '285', '山东\x01东营': '82', '江西\x01上饶': '9', '吉林\x01白城': '410', '湖北\x01黄冈': '33',
        '新疆\x01阿克苏': '315', '山西\x01晋城': '234', '安徽\x01蚌埠': '187', '江苏\x01无锡': '127', '湖北\x01咸宁': '40',
        '黑龙江\x01哈尔滨': '152', '山东\x01德州': '86', '浙江\x01金华': '135', '湖南\x01益阳': '48', '海南\x01海口': '239',
        '湖南\x01湘潭': '47', '湖南\x01永州': '269', '黑龙江\x01佳木斯': '320', '黑龙江\x01鸡西': '323', '湖北\x01鄂州': '39',
        '安徽\x01芜湖': '188', '全国\x01全国': '0'}

USER_AGENT = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
item = {'scenic': '14', 'travel_city': '302'}
sex = {'male': '950', 'female': '951'}
age = {'10_19': '961', '20_29': '962', '30_39': '963', '40_49': '964', '50_59': '965', '60_69': '966'}
def baidu_top():
    headers = {
        'Host': 'top.baidu.com',
        'Referer': 'http://top.baidu.com/region?fr=topindex',
        'User-Agent': random.choice(USER_AGENT),
        'X-Requested-With': 'ShockwaveFlash/25.0.0.127'
    }
    url = 'http://top.baidu.com/region/singlelist'
    session = requests.session()
    # 一次选3个城市,一共339个
    cities = (each for each in city.keys())
    ages = (each2 for each2 in age.keys())
    #抓年龄
    for i in range(2):
        age1 = ages.__next__()
        age2 = ages.__next__()
        age3 = ages.__next__()
        for t in item.keys():
            data = {
                'boardid': item[t],
                'divids[0]': age[age1],
                'divids[1]': age[age2],
                'divids[2]': age[age3]
            }
            time.sleep(2)
            try:
                response = session.post(url, headers=headers, data=data, timeout=30).text
            except:
                time.sleep(60)
                continue
            jsDict = json.loads(response)
            ids = jsDict["topWords"]
            for id in ids:
                cons = jsDict["topWords"][str(id)]
                if id == age[age1]:
                    name = age1
                elif id == age[age2]:
                    name = age2
                else:
                    name = age3
                for each in cons:
                    trend = each["trend"]
                    searches = each["searches"]
                    changeRate = each["changeRate"]
                    isNew = each["isNew"]
                    keyword = each["keyword"]
                    percentage = each["percentage"]
                    text = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (
                    name, '\u0001', trend, '\u0001', searches, '\u0001', changeRate,
                    '\u0001', isNew, '\u0001', keyword, '\u0001', percentage, '\u0001')
                    save(text, t + '_ages', HDFS)
    #抓性别
    for t in item.keys():
        data = {
            'boardid': item[t],
            'divids[0]': sex["male"],
            'divids[1]': sex["female"],
            'divids[2]': '1'
        }
        time.sleep(2)
        try:
            response = session.post(url, headers=headers, data=data, timeout=30).text
        except:
            time.sleep(60)
            continue
        jsDict = json.loads(response)
        ids = jsDict["topWords"]
        for id in ids:
            if id == '1':
                continue
            else:
                cons = jsDict["topWords"][str(id)]
                if id == sex['male']:
                    name = "male"
                elif id == sex["female"]:
                    name = "female"
                for each in cons:
                    trend = each["trend"]
                    searches = each["searches"]
                    changeRate = each["changeRate"]
                    isNew = each["isNew"]
                    keyword = each["keyword"]
                    percentage = each["percentage"]
                    text = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (
                    name, '\u0001', trend, '\u0001', searches, '\u0001', changeRate,
                    '\u0001', isNew, '\u0001', keyword, '\u0001', percentage, '\u0001')
                    save(text, t + '_sex', HDFS)
    #各个城市
    for i in range(112):
        name1 = cities.__next__()
        name2 = cities.__next__()
        name3 = cities.__next__()
        '''旅游城市:302,风景名胜:14,'''
        for t in item.keys():
            data = {
                'boardid': item[t],
                'divids[0]': city[name1],
                'divids[1]': city[name2],
                'divids[2]': city[name3]
            }
            time.sleep(2)
            try:
                response = session.post(url, headers=headers, data=data, timeout=30).text
            except:
                time.sleep(60)
                continue
            jsDict = json.loads(response)
            ids = jsDict["topWords"]
            for id in ids:
                cons = jsDict["topWords"][str(id)]
                if id == city[name1]:
                    name = name1
                elif id == city[name2]:
                    name = name2
                else:
                    name = name3
                for each in cons:
                    trend = each["trend"]
                    searches = each["searches"]
                    changeRate = each["changeRate"]
                    isNew = each["isNew"]
                    keyword = each["keyword"]
                    percentage = each["percentage"]
                    text = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s' %(name, '\u0001', trend, '\u0001', searches, '\u0001', changeRate,
                                                    '\u0001', isNew, '\u0001', keyword, '\u0001', percentage, '\u0001')
                    save(text, t, HDFS)

def save(text, t, hdfs):
    n = time.strftime('%Y_%m_%d_%H', time.localtime(time.time()))
    #写入本地
    with open(os.path.join(os.path.abspath("Data"), n + "baiduTop_" + t + ".txt"), 'a', encoding='utf8') as f:
        f.write(text + '\n')
    # print(hdfs.exists("/user/cloudera/tmp/baidutop_base/"+n + "baiduTop_"+ t + ".txt"))
    #写入hdfs
    with hdfs.open("/user/cloudera/tmp/baidutop_base/"+ n + "baiduTop_"+ t + ".txt", 'ab') as f:
        f.write(text + '\n')





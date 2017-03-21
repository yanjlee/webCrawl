# coding=utf8

import requests
import time
import json
from lxml import etree
def run():
    session = requests.session()
    headers = {
        'Host': 'hotel.elong.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
    }
    url = 'http://hotel.elong.com/ajax/list/asyncsearch'
    cookies = session.get(url, headers=headers).cookies

    data = {
        'listRequest.areaID': 100408944,
        'listRequest.cityID': '0820',
        'listRequest.cityName': '葫芦岛',
        'listRequest.pageIndex': 20,
        'listRequest.pageSize': 20

    }

    response = session.post(url, headers=headers, data=data, cookies=cookies)
    print(response.text)


def run2():
    session = requests.session()
    headers = {
        'Host': 'hotel.elong.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        'Referer': 'http://hotel.elong.com/chengdu/02301481/',
        'X-Requested-With': 'XMLHttpRequest'
    }
    data = {
        # 'code': '2031904003_45b99e14-35ce-4a8e-ab7f-f956abd1d2bc',
        # 'detailRequest.bookingChannel': "1",
        # 'detailRequest.cardNo': "192928",
        'detailRequest.checkInDate': '2017-04-01',
        'detailRequest.checkOutDate': '2017-04-02',
        'detailRequest.cityId': '2301',
        'detailRequest.citySeoNameEn': 'chengdu',
        'detailRequest.customerLevel': "11",
        'detailRequest.hotelIDs': '02301481',
        # 'detailRequest.isAfterCouponPrice': 'true',
        # 'detailRequest.isDebug': 'false',
        # 'detailRequest.isLogin': 'false',
        # 'detailRequest.isMobileOnly': "false",
        # 'detailRequest.isNeed5Discount': "false",
        # 'detailRequest.isTrace': "false",
        # 'detailRequest.language': "cn",
        # 'detailRequest.needDataFromCache': "true",
        # 'detailRequest.orderFromID': "50",
        # 'detailRequest.productType': "0",
        # 'detailRequest.promotionChannelCode': "0000",
        # 'detailRequest.proxyID': 'ZD',
        # 'detailRequest.sellChannel': "1",
        # 'detailRequest.settlementType': "0",
        # 'detailRequest.updateOrder': 'false'
    }
    url = 'http://hotel.elong.com/ajax/detail/gethotelroomsetjva'
    # url2 = 'http://hotel.elong.com/ajax/detail/getcode.html?hotelId=02301481&_=1490076005949'
    # url3 = 'http://hotel.elong.com/chengdu/02301481/'
    # # r1 = session.get(url3, headers=headers)
    # # print(r1.cookies)
    # # session.cookies.update(r1.cookies)
    # # r2 = session.get(url2, headers=headers)
    # # print(r2.text)
    r3 = session.post(url, data=data, headers=headers)
    # print(r3.text)
    jsDict = json.loads(r3.text)
    print(jsDict)
    # jc = jsDict["value"]["hotelTipInfo"]["productsInfo"]
    # for each in jc:
    #     print(each)
    jcon = json.loads(r3.text)["value"]["content"]
    # print(jcon)
    selector = etree.HTML(jcon)
    content = selector.xpath('//div[@class="htype_item on"]')

    for each in content:
        f = ''
        #类型
        rtype = each.xpath('div[2]/div[3]/p[1]/span/text()')
        f += rtype[0] + '\u0001'
        #数据
        con = each.xpath('div[2]/div[3]/p[2]/span')

        for n in con:
            if n.xpath('i'):
                t = n.xpath('text()')[0].replace('\n', '')
                tt = len(n.xpath('i'))
                f += t + str(tt) + '人'
            else:
                f += n.xpath('text()')[0].replace('\n', '').replace('|', '\u0001')
        #价格
        f += '\u0001' + each.xpath('div[2]/div[2]/p[1]')[0].xpath('string(.)').replace('\n', '').replace(' ', '')
        #额外信息
        f += '\u0001' + each.xpath('div[3]/table/tbody/tr[@class="ht_tr_other"]/td[2]')[0].xpath('string(.)').\
            replace('\n', '').replace('\t', '').replace('\r', '')
        print(f)



run2()
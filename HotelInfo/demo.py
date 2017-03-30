# coding=utf8

import json
import requests
from lxml import etree

def run():
    headers = {
        'Host': 'hotels.ctrip.com',
        'Referer': 'http://hotels.ctrip.com/hotel/chengdu28',
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    }
    url = 'http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx'
    data = {
        'cityId': '28',
        'cityPY': 'chengdu',
        'location': '270',
        'page': '40'
    }
    response = requests.post(url, data=data, headers=headers)
    print(response.text)
    hotelList = json.loads(response.text)["hotelIds"]
    if hotelList != '':
        for each in hotelList.split(','):
            print(each.split('_')[0])
    else:
        print('done')




run()

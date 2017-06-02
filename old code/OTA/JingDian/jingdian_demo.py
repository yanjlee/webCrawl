# coding=utf8

import requests
import json

def run():
    url = 'http://search.piao.qunar.com/sight/suggestWithId.jsonp?&key=雁荡山'
    r = requests.get(url).text
    print(r)
    jsDict = json.loads(r)['data']['s']
    print(jsDict)
    for i in jsDict:
        print(i.split(','))

    url2 = 'http://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=9597&index=1&page=1&pageSize=2'

run()
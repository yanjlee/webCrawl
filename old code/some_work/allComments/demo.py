# coding:utf8

import requests, os
import json
from hdfs3 import HDFileSystem
from hdfs.client import Client
def run():
    headers = {
        'Host': 'hotel.elong.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    url = 'http://hotel.elong.com/ajax/detail/gethotelreviews'
    parmams = {
        'hotelId': '42309003',
        'pageIndex': '2',
        'code': '-99'
    }
    # response = requests.get(url, headers=headers, params=parmams)
    # print(response.text)
    with open(os.path.join(os.path.abspath("Data"), "elong_hotel_list.txt"), 'r', encoding='utf8') as text:
        print(text.__next__())

def run2():
    # hdfs = HDFileSystem('cdh5namenode', '8020')
    hdfs = HDFileSystem(host='192.168.100.178', port=8020)
    hdfs.mkdir('/user/cloudera/tmp/trave_hotel/test/')
    # client = Client("http://192.168.100.78:50070")  # 50070: Hadoop默认namenode
    with hdfs.open("/user/cloudera/tmp/trave_hotel/elong_comment.txt", 'ab') as f:
        f.write('hello' + '\n')

run2()
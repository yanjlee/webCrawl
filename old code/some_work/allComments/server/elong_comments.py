# -*- coding:utf-8 -*-

import requests, queue, threading
import time, os, json, random

class Elong:
    def __init__(self):
        pass
    def run(self):
        return self.do_schedule()
    def do_schedule(self):
        '''首先从酒店列表里拿到数据,然后再一次进入对应酒店,开始存放数据'''
        if True:
            t_generator = Elong_threads_for_input_generator()
            t_generator.start()
            t_generator.join()
            #把生成器提取出来
            generator = queue_generator.get()
            for i in range(1):
                t_hids = Elong_threads_for_input_hid(generator)
                t_hids.start()
                t_hids.join()
                #从队列里提取数据,开始抓取评论数据
                while not queue_hids.empty():
                    t_json = Elong_threads_for_get_hid()
                    t_json.start()
                    t_json.join()
                    while not queue_json.empty():
                        t_spyder = Elong_threads_for_get_data()
                        t_spyder.start()

class headers:
    '''构造普通ua'''
    def __init__(self):
        self.USER_AGENT = [
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
    def make_headers(self, content):
        headers = {
            'Host': content,
            'User-Agent': random.choice(self.USER_AGENT),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

        return headers
    '''构造特殊ua'''
    def updata_headers(self, content, newKey, newValue):
        headers = {
            'Host': content,
            'User-Agent': random.choice(self.USER_AGENT),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        headers[newKey] = newValue
        return headers

class Elong_session:
    def __init__(self):
        self.headers = headers()
        self.session = requests.session()
    def get_info(self, hid, n):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/ajax/detail/gethotelreviews'
        headers = self.headers.updata_headers(host, 'X-Requested-With', 'XMLHttpRequest')
        time.sleep(1.5)
        params = {
            'hotelId': hid,
            'pageIndex': n,
            'code': '-99'
        }
        '''这里要返回,对page的大小做一个判断'''
        proxy = {
            'http': '112.91.135.115:8080',
            'http': '171.8.79.143:8080'
        }
        try:
            return self.session.get(url, headers=headers, params=params, proxies=proxy, timeout=30).text
        except:
            return False


queue_generator = queue.Queue(0)
queue_hids = queue.Queue(0)
queue_json = queue.Queue(0)

class Elong_threads_for_input_generator(threading.Thread):
    '''将酒店生成器放入队列'''
    def __init__(self):
        super(Elong_threads_for_input_generator, self).__init__()
    def run(self):
        text = open(os.path.join(os.path.abspath("Data"), "elong_hotel_list.txt"), 'r', encoding='utf8')
        queue_generator.put(text)
        queue_generator.task_done()
class Elong_threads_for_input_hid(threading.Thread):
    '''将酒店id放入队列'''
    def __init__(self, generator):
        super(Elong_threads_for_input_hid, self).__init__()
        self.generator = generator
    def run(self):
        each = self.generator.__next__()
        queue_hids.put(deal_hids_elong(each))
        queue_hids.task_done()



class Elong_threads_for_get_hid(threading.Thread):
    '''将酒店hid获取,放入session队列'''
    def __init__(self):
        super(Elong_threads_for_get_hid, self).__init__()
    def run(self):
        hid = queue_hids.get()
        #首先获取评论页数
        json_data = get_info(hid, 1)
        if json_data:
            queue_json.put([json_data, hid])
            queue_json.task_done()
            #确定评论页数
            n = deal_json_get_page_num(json_data)
            i = 2
            while i <=n:
                data = get_info(hid, i)
                queue_json.put([data, hid])
                print('ok')
                queue_json.task_done()
                i += 1

class Elong_threads_for_get_data(threading.Thread):
    '''从队列里提取json数据,开始获取数据'''
    def __init__(self):
        super(Elong_threads_for_get_data, self).__init__()
    def run(self):
        info = queue_json.get()
        get_data(info[0], info[1])
class Elong_pipeline:
    def deal_hids_elong(self, data):
        return data.split('\u0001')[5]

    def deal_json_get_page_num(self, content):
        try:
            num = json.loads(content)["totalNumber"]
            if int(num/20) < num/20:
                return int(num/20 + 1)
            else:
                return  int(num/20)
        except Exception as e:
            print(e)
            return 1

    def get_data(self, info):
        hid = info["hid"]
        nickName = info["nickName"]
        content = info["content"].replace('\n', '')
        recomend = info["recomend"]
        if recomend == 1:
            recomend = '好评'
        elif recomend == 2:
            recomend = '差评'
        roomTypeName = info["roomTypeName"].replace('\n', '')
        createTimeString = info["createTimeString"].replace('\n', '')
        text = '%s%s%s%s%s%s%s%s%s%s%s%s' %(hid, '\u0001', nickName, '\u0001', content, '\u0001', recomend, '\u0001',
                                            roomTypeName, '\u0001', createTimeString, '\u0001')
        #保存数据
        with open(os.path.join(os.path.abspath("Data")," elong_comment.txt"), 'a', encoding='utf8') as f:
            f.writelines(text + '\n')

class Elong_spyder:
    def __init__(self):
        self.pipeline = Elong_pipeline()
    def get_data(self, contents, hid):
        try:
            jsDict = json.loads(contents)["contents"]
            info = {}
            info["hid"] = hid
            for each in jsDict:
                info["recomend"] = each["recomend"]
                info["content"] = each["content"]
                info["createTimeString"] = each["createTimeString"]
                info["nickName"] = each["commentUser"]["nickName"]
                info["roomTypeName"] = each["commentExt"]["order"]["roomTypeName"]
                self.pipeline.get_data(info)
        except Exception as e:
            print(e)
#处理hid
elp = Elong_pipeline()
def deal_hids_elong(data):
    return elp.deal_hids_elong(data)
def deal_json_get_page_num(json):
    return elp.deal_json_get_page_num(json)
#处理session
els = Elong_session()
def get_info(hid, n):
    return els.get_info(hid, n)
#获取数据
elc = Elong_spyder()
def get_data(json, hid):
    return elc.get_data(json, hid)

if __name__ == '__main__':
    elong_spyder = Elong()
    elong_spyder.run()
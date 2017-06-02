# coding=utf8

import threading, queue, os
from piplines import Elong_pipeline
from sessions import Elong_session
from hdfs3 import HDFileSystem
from spyder.Elong_spyder import Elong_spyder

#**************************艺龙网******************************************************************************
queue_generator = queue.Queue()
queue_hids = queue.Queue()
queue_json = queue.Queue()
queue_data = queue.Queue()
lock = threading.Lock()
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
        # if json_data:
        #     get_data(json_data, hid)
        #     n = deal_json_get_page_num(json_data)
        #     i = 2
        #     while i <= n:
        #         data = get_info(hid, i)
        #         get_data(data, hid)
        #         i += 1
        if json_data:
            queue_json.put([json_data, hid])
            queue_json.task_done()
            #确定评论页数
            n = deal_json_get_page_num(json_data)
            i = 2
            while i <=n:
                # print(str(i) + 'a')
                data = get_info(hid, i)
                queue_json.put([data, hid])
                queue_json.task_done()
                i += 1

class Elong_threads_for_get_data(threading.Thread):
    '''从队列里提取json数据,开始获取数据'''
    def __init__(self):
        super(Elong_threads_for_get_data, self).__init__()
    def run(self):
        info = queue_json.get()
        get_data(info[0], info[1])

class Elong_threads_for_input_data(threading.Thread):
    def __init__(self):
        super(Elong_threads_for_input_data, self).__init__()
    def run(self):
        text = queue_data.get()
        save_as_comments(text)
#处理hid
elp = Elong_pipeline()
def deal_hids_elong(data):
    return elp.deal_hids_elong(data)
def deal_json_get_page_num(json):
    return elp.deal_json_get_page_num(json)
def save_as_comments(text):
    # lock.acquire()
    return elp.save_as_comments(text, HDFS)
    # lock.release()
#处理session
els = Elong_session()
def get_info(hid, n):
    return els.get_info(hid, n)
#获取数据
elc = Elong_spyder()
def get_data(json, hid):
    return elc.get_data(json, hid)
#处理队列数据
def deal_queue(text):
    queue_data.put(text)
    queue_data.task_done()

global HDFS
HDFS = HDFileSystem(host='192.168.100.178', port=8020)
#******************************************************************************************************************

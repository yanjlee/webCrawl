# coding=utf8

'''
Info:
- author    : wangjiawei
- email     : wangjw@daqsoft.com.cn
- date      : 2017,03,20
Update:
- name      :
- email     :
- date      :
'''

from session import makeSession
from spyder.Ctrip_spyder import ctrip_spyder
from pipeline import Ctrip_pipe
import threading, time, queue, os
from hdfs3 import HDFileSystem

que_data_h = queue.Queue()
que_data_r = queue.Queue()
global HDFS
HDFS = HDFileSystem(host='192.168.100.178', port=8020)

class Ctrip_schedule():
    #初始化各类全局变量
    def __init__(self):
        self.que_cities = queue.Queue()
        self.que_city_html = queue.Queue()
        self.que_city_list = queue.Queue()
        self.que_hotel_list = queue.Queue()
        self.que_hotel_info = queue.Queue()
        self.que_room_info = queue.Queue()
        self.session = makeSession()
        self.spyder = ctrip_spyder()
        self.pipeline = Ctrip_pipe()
        self.lock = threading.Lock()
        #调用,还是用成员变量,不用函数
        self.do_get_code = False
        self.do_get_city_info = False
        self.do_get_hotel_list = False
        self.do_get_htl_and_rm_info = False
    '''之所以留下run()这个鸡肋方法，是为了在调用时候方便'''
    def run(self):
        return self.do_schedule()

    def do_schedule(self):
        '''
        作为调度般的存在
        :return:
        '''
        #抓取城市code
        if self.do_get_code:
            self.threading_for_Ctrip_home_page() #爬取携程的主页
        # 抓取行政区
        if self.do_get_city_info:
            self.threading_for_Ctrip_each_cities()
            self.threading_for_deal_queue_cities()
            #数据放入队列后
            while not self.que_cities.empty():
                self.threading_for_get_city_html()
                while not self.que_city_html.empty():
                    self.threading_for_city()

        #抓取酒店列表
        if self.do_get_hotel_list:
            self.threading_for_put_cities_in_queue()
            while not self.que_city_list.empty():
                self.threading_for_get_hotel_list_html()
                while not self.que_hotel_list.empty():
                    self.threading_for_spyder_hotel_list()

        #抓取酒店数据
        if self.do_get_htl_and_rm_info:
            #把酒店列表放入队列
            self.threading_for_put_hotel_list_in_queue()
            #开始抓取数据
            while not self.que_hotel_list.empty():
                hid = self.que_hotel_list.get()
                print(hid)
                self.threading_for_hotel_info(hid)
                self.threading_for_room_info(hid)
                while not self.que_hotel_info.empty():
                    self.threading_for_spyder_hotel_info()
                    self.threading_for_spyder_room_info()
                    while not que_data_h.empty():
                        self.threading_for_input_hotel_data()
                        self.threading_for_input_room_data()
    def threading_for_input_hotel_data(self):
        td_s_htl = threading.Thread(target=self.save_data_as_htl, args=(que_data_h.get(),))
        td_s_htl.start()
        td_s_htl.join()
    def threading_for_input_room_data(self):
        td_s_htl = threading.Thread(target=self.save_data_as_room, args=(que_data_r.get(),))
        td_s_htl.start()
        td_s_htl.join()
    def threading_for_Ctrip_home_page(self):
        '''
        创建一个线程,来实现对携程主页的爬取,并将对应的城市以及id写入文件
        :return:
        '''
        td_home_page = threading.Thread(target=self.get_info_from_Ctrip_home_page)
        td_home_page.start()
        td_home_page.join()
    def threading_for_Ctrip_each_cities(self):
        '''
        创建1个线程，来完成对页面的爬取,获取每个城市的行政区以及附属县市
        :return:
        '''
        td_each_city = threading.Thread(target=self.deal_each_city)
        td_each_city.start()
        td_each_city.join()
    def threading_for_deal_queue_cities(self):
        td_que_c = threading.Thread()
        for each in self.que_cities.get():
            td_que_c = threading.Thread(target=self.deal_each_city_into_dict, args=(each,))
            td_que_c.start()
            td_que_c.join()
    def threading_for_get_city_html(self):
        '''
        四个线程开始抓取
        :return:
        '''
        time.sleep(1)
        th_get_city_html = threading.Thread(target=self.get_city_html, args=(self.que_cities.get(),))
        time.sleep(1)
        th_get_city_html2 = threading.Thread(target=self.get_city_html, args=(self.que_cities.get(),))
        time.sleep(1)
        th_get_city_html3 = threading.Thread(target=self.get_city_html, args=(self.que_cities.get(),))
        time.sleep(1)
        th_get_city_html4 = threading.Thread(target=self.get_city_html, args=(self.que_cities.get(),))
        th_get_city_html.start()
        th_get_city_html2.start()
        th_get_city_html3.start()
        th_get_city_html4.start()
        th_get_city_html.join()
        th_get_city_html2.join()
        th_get_city_html3.join()
        th_get_city_html4.join()
    def threading_for_city(self):
        '''
        作为spyder的存在,这里并没有把spyder和pipline分开,而是当做同一个来处理的
        :return:
        '''
        th_get_data_from_city_html = threading.Thread(target=self.spyder_for_city_html, args=(self.que_city_html.get(),))
        th_get_data_from_city_html.start()
    def threading_for_put_cities_in_queue(self):
        '''
        把各城市行政区和附属县市放入队列
        :return:
        '''
        for i in open(os.path.join(os.path.abspath("Data"), "Ctrip_city_fs.txt"), 'r', encoding='utf8'):
            self.que_city_list.put(self.pipeline.deal_each_area_code(i))
    def threading_for_get_hotel_list_html(self):
        '''
        四个线程开始抓取
        :return:
        '''
        th_get_hotel_html = threading.Thread(target=self.get_hotel_html, args=(self.que_city_list.get(),))
        th_get_hotel_html.start()
        th_get_hotel_html.join()


    def threading_for_spyder_hotel_list(self):
        '''
        四个线程跑spyder
        :return:
        '''
        th_get_data_for_hotel_list = threading.Thread(target=self.spyder_for_hotel_list, args=(self.que_hotel_list.get(),))
        th_get_data_for_hotel_list.start()

    def threading_for_put_hotel_list_in_queue(self):
        '''
        把hotel_list里的数据放入queue_list
        :return:
        '''
        n = 0
        for i in open(os.path.join(os.path.abspath("Data"), "Ctrip_hotel_list.txt"), 'r', encoding='utf8').readlines():
            n += 1
            if n < 37630:
                continue
            else:
                self.que_hotel_list.put(self.pipeline.deal_each_hotel_id(i))
                self.que_hotel_list.task_done()

    def threading_for_hotel_info(self, hid):
        '''
        一个线程来跑parser
        :param hid:
        :return:
        '''
        time.sleep(2)
        th_htl_info = threading.Thread(target=self.get_hotel_info, args=(hid,))
        th_htl_info.start()
    def threading_for_room_info(self, hid):
        '''
        一个线程来跑parser
        :param hid:
        :return:
        '''
        time.sleep(2)
        th_rom_info = threading.Thread(target=self.get_room_info, args=(hid,))
        th_rom_info.start()
        th_rom_info.join()
    def threading_for_spyder_hotel_info(self):
        '''
        一个线程来跑爬虫数据
        :return:
        '''
        th_room_info = threading.Thread(target=self.spyder_for_hotel_info, args=(self.que_hotel_info.get(),))
        th_room_info.start()

    def threading_for_spyder_room_info(self):
        '''
        一个线程来跑爬虫数据
        :return:
        '''
        th_room_info = threading.Thread(target=self.spyder_for_room_info, args=(self.que_room_info.get(),))
        th_room_info.start()
    def get_info_from_Ctrip_home_page(self):
        '''
        作为从携程主页提取出a-z的城市以及相应代码,并保存在Data/Ctrip_cities_code.txt里
        :return:
        '''
        self.lock.acquire()
        self.spyder.get_data_of_cities(self.session.get_home_page_from_Ctrip())
        self.lock.release()
    def get_city_html(self, city):
        '''
        建立session,爬取各个城市的数据html放入队列
        :param city: 城市的数据被放在字典里
        :return:
        '''
        city_html = self.session.get_city_html(city)
        if city_html:
            self.que_city_html.put(city_html)
            #print('each city html already put in')
    def get_hotel_html(self, content):
        self.lock.acquire()
        '''
        建立session,爬取各城市酒店列表，并放入队列
        :return:
        '''
        if content:
            n = 1
            while True:
                hotel_html = self.session.get_hotel_list(content, n)
                if hotel_html:
                    if self.pipeline.do_judge(hotel_html):
                        n += 1
                        self.que_hotel_list.put([content, hotel_html])
                        #print('hotel list already put in', n-1)
                    else:
                        break
                else:
                    n += 1
                    continue
        self.lock.release()
    def get_hotel_info(self, hid):
        '''
        建立session,获取酒店的html
        :param hid:
        :return:
        '''
        if hid:
            htl_info = self.session.get_hoel_info(hid)
            if htl_info:
                self.que_hotel_info.put([htl_info, hid])
                self.que_hotel_info.task_done()
                #print('an info of hotel has put in')
            else:
                #print(htl_info)
                self.que_hotel_info.put('no_data')
    def get_room_info(self, hid):
        '''
        建立session,获取房间的html
        :param hid:
        :return:
        '''
        if hid:
            rom_info = self.session.get_room_info(hid)
            if rom_info:
                self.que_room_info.put([rom_info, hid])
                self.que_room_info.task_done()
                #print('an info of room has put in')
            else:
                #print(rom_info)
                self.que_room_info.put('no_data')
    def deal_each_city(self):
        '''
        拿到数据,写入队列
        :return:
        '''
        self.que_cities.put(self.pipeline.deal_each_city())
        self.que_cities.task_done()
    def deal_each_city_into_dict(self, content):
        '''
        处理城市数据,写入字典
        :param content:
        :return:
        '''
        self.que_cities.put(self.pipeline.deal_each_city_into_dict(content))
        self.que_cities.task_done()
    def spyder_for_city_html(self, content):
        '''
        转跳spyder,拿数据
        :param content: 页面html
        :return:
        '''
        self.spyder.get_xzq_data(content)
    def spyder_for_hotel_list(self, content):
        '''
        转跳spyder
        :param content:
        :return:
        '''
        self.spyder.get_data_from_json(content[0], content[1])

    def spyder_for_hotel_info(self, content):
        '''
        转跳spyder,捕获酒店数据
        :param content:
        :return:
        '''
        try:
            if content !='no_data':
                #print('hotel info ok')
                self.spyder.get_hotel_data(content[0], content[1])
        except Exception as e:
            print(e)
    def spyder_for_room_info(self, content):
        '''
        转跳spyder,捕获房间数据
        :param content:
        :return:
        '''
        try:
            if content != 'no_data':
                #print('room info ok')
                self.spyder.get_room_data(content[0], content[1])
        except Exception as e:
            print(e)

    def save_data_as_htl(self, text):
        self.lock.acquire()
        try:
            self.pipeline.sava_as_hotel_info(text, HDFS)
        except Exception as e:
            print(e)
        self.lock.release()
    def save_data_as_room(self, text):
        self.lock.acquire()
        try:
            self.pipeline.save_as_room_info(text, HDFS)
        except Exception as e:
            print(e)
        self.lock.release()
def put_in_queue_htl(text):
    que_data_h.put(text)
    que_data_h.task_done()

def put_in_queue_rm(text):
    que_data_r.put(text)
    que_data_r.task_done()
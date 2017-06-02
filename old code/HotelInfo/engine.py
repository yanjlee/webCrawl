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

from HotelInfo.session import makeSession
from HotelInfo.spyder.Elong_spyder import Elong_spyder
from HotelInfo.spyder.Ctrip_spyder import ctrip_spyder
from HotelInfo.pipeline import Ctrip_pipe
import threading, time, queue, os

class Ctrip_schedule():
    #初始化各类全局变量
    def __init__(self):
        self.que_cities = queue.Queue(0)
        self.que_city_html = queue.Queue(0)
        self.que_city_list = queue.Queue(0)
        self.que_hotel_list = queue.Queue(0)
        self.que_hotel_info = queue.Queue(0)
        self.que_room_info = queue.Queue(0)
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
            while self.que_hotel_list.empty():
                hid = self.que_hotel_list.get()
                self.threading_for_hotel_info(hid)
                self.threading_for_room_info(hid)
                while self.que_hotel_info.empty():
                    self.threading_for_spyder_hotel_info()
                    self.threading_for_spyder_hotel_info()
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
        for i in open(os.path.join(os.path.abspath("Data"), "Ctrip_city_zxq.txt"), 'r', encoding='utf8'):
            self.que_city_list.put(self.pipeline.deal_each_area_code(i))
        for i in open(os.path.join(os.path.abspath("Data"), "Ctrip_city_fs.txt"), 'r', encoding='utf8'):
            self.que_city_list.put(self.pipeline.deal_each_area_code(i))
    def threading_for_get_hotel_list_html(self):
        '''
        四个线程开始抓取
        :return:
        '''
        time.sleep(1)
        th_get_hotel_html = threading.Thread(target=self.get_hotel_html, args=(self.que_city_list.get(),))
        time.sleep(1)
        th_get_hotel_html2 = threading.Thread(target=self.get_hotel_html, args=(self.que_city_list.get(),))
        time.sleep(1)
        th_get_hotel_html3 = threading.Thread(target=self.get_hotel_html, args=(self.que_city_list.get(),))
        time.sleep(1)
        th_get_hotel_html4 = threading.Thread(target=self.get_hotel_html, args=(self.que_city_list.get(),))
        th_get_hotel_html.start()
        th_get_hotel_html2.start()
        th_get_hotel_html3.start()
        th_get_hotel_html4.start()
        th_get_hotel_html.join()
        th_get_hotel_html2.join()
        th_get_hotel_html3.join()
        th_get_hotel_html4.join()

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
        for i in open(os.path.join(os.path.abspath("Data"), "Ctrip_hotel_list.txt"), 'r', encoding='utf8'):
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
        th_room_info = threading.Thread(target=self.spyder_for_room_info, args=(self.que_hotel_info.get(),))
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
            print('each city html already put in')
    def get_hotel_html(self, content):
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
                        print('hotel list already put in')
                    else:
                        break
                else:
                    n += 1
                    continue
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
                print('an info of hotel has put in')
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
                print('an info of room has put in')
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
        self.spyder.get_hotel_data(content[0], content[1])
    def spyder_for_room_info(self, content):
        '''
        转跳spyder,捕获房间数据
        :param content:
        :return:
        '''
        self.spyder.get_room_data(content[0], content[1])


class Elong(object):
    '''
    作为艺龙的酒店数据引擎,先是获取城市列表,再根据列表开始抓数据.
    '''
    def __init__(self):
        self.CHECK = True
        self.response = makeSession()
        self.esp = Elong_spyder()
    '''从json中拿到城市列表'''
    def run_city(self):
        return self.get_cityList_from_json()

    def get_cityList_from_json(self):
        host = 'openapi.elong.com'
        for i in range(2,7):
            url = 'http://openapi.elong.com/suggest/hotcity/hotel/'+ str(i) +'.html'
            r = self.response.get_Json_data_fromElong(host, url)
            self.deal_json(r)

    def deal_json(self, r):
        self.esp.getDataFromJson(r)

    '''拿到各个城市的行政区'''
    def run_xzq(self):
        return self.get_xzqList_from_cities()

    def get_xzqList_from_cities(self):
        #先获得城市列表
        t = open('Data/Elong_citiesList.txt', 'r', encoding='utf8').readlines()
        for i in range(len(t)):
            print(i)
            list = t[i].split('\u0001')
            id = list[0]
            nc = list[1]
            ne = list[2].replace('\n', '')
            self.getHtml(id, nc, ne)

    def getHtml(self, id, nc, ne):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/' + ne + '/'
        r = self.response.get_xzq_fromElong(host, url)
        self.deal_html(r, id, nc, ne)
    def deal_html(self,content, id, nc, ne):
        self.esp.getHtmlFromContent(content, id, nc, ne)
    '''从各个城市行政区出发,拿到酒店列表'''
    def run_hotelList(self):
        return self.get_hotelList_from_xzq()

    def get_hotelList_from_xzq(self):
        #先拿到行政区列表
        t = open('Data/Elong_xzqList.txt', 'r', encoding='utf-8').readlines()
        for i in range(len(t)):
            print(i)
            list = t[i].split('\u0001')
            cityid = list[0]
            citync = list[1]
            cityne = list[2]
            xzqnc = list[3]
            xzqid = list[4]
            self.get_HotelList_from_json(cityid, citync, xzqnc, xzqid, cityne)

    def get_HotelList_from_json(self, cityid, citync, xzqnc, xzqid, cityne):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/ajax/list/asyncsearch'
        n = 1
        while self.CHECK:
            r = self.response.get_hotelList_fromElong(host, url, cityid, citync, xzqid, n)
            if r:
                self.CHECK = self.do_judge_for_circle(r)
                if self.CHECK:
                    self.deal_HotelList_from_json(r, cityid, citync, xzqnc, xzqid, cityne)
                    n += 1
            else:
                self.CHECK = False
        self.CHECK = True

    def do_judge_for_circle(self, content):
        '''这里要返回一个结果,让循环继续还是停止'''
        return self.esp.do_judge(content)

    def deal_HotelList_from_json(self, content,cityid, citync, xzqnc, xzqid, cityne):
        self.esp.deal_json_for_hotelList(content, cityid, citync, xzqnc, xzqid, cityne)

    '''开始拿酒店信息'''
    def run_hotelInfo(self):
        return self.set_up_circle()
    def set_up_circle(self):
        t = open('Data/Elong_hotelList.txt', 'r', encoding='utf-8').readlines()
        for i in range(len(t)):
        # for i in range(7,9):
            list = t[i].split('\u0001')
            cid = list[0]
            cnc = list[1]
            cne = list[2]
            aid = list[3]
            anc = list[4]
            hid = list[5]
            # self.get_hotel_base_data(cnc, cne, aid, anc, hid)
            self.get_hotel_room_data(cne, hid, cid, anc, cnc)
            break
    def get_hotel_base_data(self, cnc, cne, aid, anc, hid):
        host = 'hotel.elong.com'
        url = 'http://hotel.elong.com/' + cne + '/' + hid + '/'
        r = self.response.get_info_from_hotel(host, url)
        self.deal_hotel_base_data(r, cnc, anc, hid)

    def deal_hotel_base_data(self, content, cnc, anc, hid):
        self.esp.get_hotel_base_data(content, cnc, anc, hid)

    def get_hotel_room_data(self, cne, hid, cid, anc, cnc):
        r = self.response.post_data_2_get_room_info(cne, hid, cid)
        self.deal_hotel_room_data(r, cnc, anc, hid)

    def deal_hotel_room_data(self, r, cnc, anc, hid):
        self.esp.get_hotel_room_data(r, cnc, anc, hid)

# class Ctrip_hotel_engine:
#     def __init__(self):
#         self.que_1 = queue.Queue()
#         self.que_2 = queue.Queue()
#         self.que_3 = queue.Queue()
#         self.que_4 = queue.Queue()
#         self.que_5 = queue.Queue()
#         self.que_6 = queue.Queue()
#         self.response = makeSession()
#         self.csp = ctrip_spyder()
#         self.pipeline = Ctrip_pipe()
#         self.lock = threading.Lock()
#     def run_get_cities(self):
#         return self.get_cities()
#     def get_cities(self):
#         response = self.response.get_home_page_from_Ctrip()
#         return self.load_in_data_for_cities(response)
#     '''-----------------分割线----------------'''
#     def run_get_all_cities(self):
#         '''这里作为调度器的存在'''
#         #首先是读取城市列表,并放入队列中
#         self.load_in_data_for_cities()
#         #提取数据,开始处理,并放入队列里
#         for each in self.get_data_from_que_and_deal():
#             threading.Thread(target=self.deal_each_city, args=(each,)).start()
#         num = self.que_1.qsize()
#         #从队列一提出来,开始处理并放入队列二,这里需要考虑主线程和子线程
#         n = 1
#         while n <= num:
#             time.sleep(2)
#             td = threading.Thread(target=self.get_city_html, args=(self.que_1.get(),))
#             td.start()
#             td.join()
#             n += 1
#         #从队列2里提取数据数据
#         n = 1
#         num2 = self.que_2.qsize()
#         while n <= num2:
#             td_s = threading.Thread(target=self.deal_page_for_city_info, args=(self.que_2.get(),))
#             td_s.start()
#         self.que_2.task_done()
#     def load_in_data_for_cities(self):
#         text = open(os.path.join(os.path.abspath("Data"), "Ctrip_cities_code.txt"), 'r', encoding='utf-8')
#         self.que_1.put(text, block=True, timeout=None)
#     def get_data_from_que_and_deal(self):
#         text = self.que_1.get()
#         return text
#     def deal_each_city(self, city):
#         self.lock.acquire()
#         dict = self.pipeline.deal_each_city(city)
#         self.que_1.put(dict)
#         self.lock.release()
#     def get_city_html(self, dict):
#         self.lock.acquire()
#         #将网页返回数据放入队列2中
#         self.que_2.put(self.response.get_city_html(dict), block=True, timeout=None)
#         print('put in')
#         self.lock.release()
#     def deal_page_for_city_info(self, html):
#         self.lock.acquire()
#         self.csp.get_xzq_data(html)
#         self.lock.release()
#     '''--------------------分割线--------------------------------'''
#     def run_get_hotel_list(self):
#         return self.hotel_list_schedule()
#
#     def hotel_list_schedule(self):
#         #先拿到列表,放入队列1
#         for each1 in open(os.path.join(os.path.abspath("Data"), "Ctrip_city_fs.txt"), 'r'):
#             self.que_1.put(each1)
#         for each2 in open(os.path.join(os.path.abspath("Data"), "Ctrip_city_zxq.txt"),'r'):
#             self.que_1.put(each2)
#         num = self.que_1.qsize()
#         n = 1
#         while n <= num:
#             td = threading.Thread(target=self.deal_each_area_code, args=(self.que_1.get(),))
#             td.start()
#             td.join()
#             n += 1
#         #现在开始做make session
#         n = 1
#         num2 = self.que_2.qsize()
#         while n <= num2:
#             print(n)
#             for i in range(4):
#                 time.sleep(5)
#                 td2 = threading.Thread(target=self.makeSession, args=(self.que_2.get(),))
#                 td2.start()
#                 td2.join()
#             n += 4
#
#
#     def deal_each_area_code(self, content):
#         #解析后的数据放入队列
#         self.lock.acquire()
#         self.que_2.put(self.pipeline.deal_each_area_code(content))
#         self.lock.release()
#
#     def makeSession(self, dict):
#         # self.lock.acquire()
#         if dict:
#             n = 1
#             while True:
#                 r = self.response.get_hotel_list(dict, n)
#                 if r:
#                     if self.do_judge(r):
#                         self.csp.get_data_from_fs(dict, r)
#                         n += 1
#                     else:
#                         break
#                 else:
#                     n += 1
#                     continue
#         # self.lock.release()
#     def do_judge(self, content):
#         result =  self.pipeline.do_judge(content)
#         if result:
#             return True
#         else:
#             return False
#
#     '''------------------------分割线-----------------------------'''
#     #以下就是关于酒店详细数据的抓取
#     def run_hotel_info(self):
#         return self.getHotelInfo()
#     #开始酒店数据获取流程
#     def getHotelInfo(self):
#         #首先是获取酒店列表
#         for each in open(os.path.join(os.path.abspath("Data"), "demo1.txt"), 'r'):
#             self.que_3.put(each)
#         #然后一个线程来处理
#         while True:
#             td_1 = threading.Thread(target=self.deal_each_hotel, args=(self.que_3.get(),))
#             td_1.start()
#             td_1.join()
#             if self.que_3.empty():
#                 break
#         #下面是session模块
#         n = 1
#         while n < 3:
#             for i in range(2):
#                 cons = self.que_4.get()
#                 # td_2 = threading.Thread(target=self.get_hotel_info, args=(cons,)) #hotel请求
#                 td_3 = threading.Thread(target=self.get_room_info, args=(cons,))  #room请求
#                 # td_2.start()
#                 td_3.start()
#                 if self.que_4.empty():
#                     self.que_3.task_done()
#                     break
#     def deal_each_hotel(self, content):
#         self.lock.acquire()
#         hid = self.pipeline.deal_each_hotel(content)
#         self.que_4.put(hid)
#         #队列4放入酒店的hid,后面session获取hid,同时通知spyder来抓数据
#         self.lock.release()
#     def get_hotel_info(self, hid):
#         self.lock.acquire()
#         content = self.response.get_hoel_info(hid)
#         self.csp.get_hotel_data(content, hid)
#         self.lock.release()
#     def get_room_info(self, hid):
#
#         self.lock.acquire()
#         content = self.response.get_room_info(hid)
#         self.csp.get_room_data(content, hid)
#         self.lock.release()
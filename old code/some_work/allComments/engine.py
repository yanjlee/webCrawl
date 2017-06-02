# coding=utf8

'''
Info:
- author    : wangjiawei
- email     : wangjw@daqsoft.com.cn
- date      : 2017,04,10
Update:
- name      :
- email     :
- date      :
'''
from constructs import *
'''艺龙酒店评论抓取'''


class Elong_comments:
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
            n = 0
            for i in range(278592):
            #for i in range(10):
                print(n)
                n += 1
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
                        t_spyder.join()
                        while not queue_data.empty():
                            t_data = Elong_threads_for_input_data()
                            t_data.start()
                            t_data.join()
if __name__ == '__main__':
    e = Elong_comments()
    e.run()

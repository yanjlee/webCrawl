# coding=utf8


import re


class BaiduSpyder():
    def __init__(self, column_spilt='\u0001', name=None, impression=None, description=None, map_info=None,
                 address=None, Tel=None, web=None, avgCost=None, price=None, vtime=None, btime=None, otime=None):
        self.__name = name
        self.__column_spilt = column_spilt
        self.__impression = impression
        self.__description = description
        self.__map_info = map_info
        self.__address = address
        self.__Tel = Tel
        self.__web = web
        self.__avgCost = avgCost
        self.__price = price
        self.__vtime = vtime
        self.__btime = btime
        self.__otime = otime
    #获取response
    def getResponse(self, response):
        return self.getData(response)
    #开始抓数据
    def getData(self, response):
        try:
            content0 = re.findall('wonderNotes.init(.*?)father_place', response, re.S)[0]
            #名称
            self.__name = re.findall('word: "(.*?)",', content0, re.S)[0].encode('raw_unicode_escape').decode('utf-8')
            # -------------------分割线---------------------
            content1 = re.findall('define\(\'scene(.*?)cids:', response, re.S)[0]
            #大家印象
            if re.findall('impression:"(.*?)",', content1, re.S)[0]:
                self.__impression = re.findall('impression:"(.*?)",', content1, re.S)[0].\
                    encode('utf-8').decode('unicode-escape').replace('\r\n', '').replace('\n', '')
            #描述
            if re.findall('more_desc:"(.*?)",', content1, re.S)[0]:
                self.__description = re.findall('more_desc:"(.*?)",', content1, re.S)[0].\
                    encode('utf-8').decode('unicode-escape').replace('\r\n', '').replace('\n', '')
            #坐标
            if re.findall('map_info:"(.*?)",', content1, re.S)[0]:
                self.__map_info = re.findall('map_info:"(.*?)",', content1, re.S)[0]
            #位置
            if re.findall('address:"(.*?)",', content1, re.S)[0]:
                self.__address = re.findall('address:"(.*?)",', content1, re.S)[0].\
                    encode('utf-8').decode('unicode-escape')
            #电话
            if re.findall('phone:"(.*?)",', content1, re.S)[0]:
                self.__Tel = re.findall('phone:"(.*?)",', content1, re.S)[0]
            #网址
            if re.findall('website:"(.*?)",', content1, re.S)[0]:
                self.__web = re.findall('website:"(.*?)",', content1, re.S)[0]
            #平均消费
            if re.findall('avg_cost:"(.*?)",', content1, re.S)[0]:
                self.__avgCost = re.findall('avg_cost:"(.*?)",', content1, re.S)[0]
            #--------------------分割线-----------------------
            content2 = re.findall('define\(\'cidMap(.*?)info.init\(\);', response, re.S)[0]
            #门票
            if re.findall('ticket_info\',\{text:(.*?)}', content2, re.S)[1]:
                self.__price = self.translate(re.findall('ticket_info\',\{text:(.*?)}', content2, re.S)[1])
            #游览时长
            if re.findall('bestvisittime\',\{text:(.*?)}', content2, re.S)[1]:
                self.__vtime = self.translate(re.findall('bestvisittime\',\{text:(.*?)}', content2, re.S)[1])
            #最佳观赏时间
            if re.findall('besttime\',\{text:(.*?)}', content2, re.S)[1]:
                self.__btime = self.translate(re.findall('besttime\',\{text:(.*?)}', content2, re.S)[1])
            #开放时间
            if re.findall('open_time_desc\',\{text:(.*?)}', content2, re.S)[1]:
                self.__otime = self.translate(re.findall('open_time_desc\',\{text:(.*?)}', content2, re.S)[1])
            #----------------分割线--------------------------
            # 保存数据
            self.save()
        except Exception as e:
            print(e)
    def translate(self, content):
        if content == 'null':
            return 'None'
        else:
            return content.replace('"', '').encode('utf-8').decode('unicode-escape').replace('\n', ',')
    def save(self):
        '''
        字段保存,名字+位置+门票+开放时间+最佳观赏时间+游览时长+平均消费+网址+电话+坐标+印象+描述
        '''
        text = str(self.__name) + self.__column_spilt + str(self.__address) + self.__column_spilt + str(self.__price) +\
            self.__column_spilt + str(self.__otime) + self.__column_spilt + str(self.__btime) + self.__column_spilt +\
            str(self.__vtime) + self.__column_spilt + str(self.__avgCost) + self.__column_spilt + str(self.__web) +\
            self.__column_spilt + str(self.__Tel) + self.__column_spilt + str(self.__map_info) + self.__column_spilt +\
            str(self.__impression) + self.__column_spilt + str(self.__description) + self.__column_spilt
        # print(text)
        with open('data/dataBaidu.txt', 'a', encoding='utf-8') as f:
            print(self.__name)
            f.writelines(text + '\n')
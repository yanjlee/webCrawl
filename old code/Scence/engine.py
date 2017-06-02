# coding=utf8

from Scence.session import setUpSession
from Scence.config import PROVINCE
from Scence.pipeline import qunar_pipline
from Scence.spyder.qunar_spyder import qunarSpyder
'''去哪儿网的全国景点列表'''
class qunar():
    def __init__(self):
        self.session = setUpSession()
        self.pipline = qunar_pipline()
        self.spyder = qunarSpyder()
    def run(self):
        return self.makeSession()

    def makeSession(self):
        for prov in PROVINCE:
            n = 1
            while True:
                print(n,prov)
                response = self.session.get_searchJson_from_qunar(prov, n)
                #这里需要一个判断,如果网页打不开就要返回一个False
                if response:
                    check = self.dealJson(response, n)
                    if check:
                        n += 1
                        continue
                    else:
                        break
                else:
                    n += 1  #如果不让n自增1,就会造成直到这个页面加载出来才通过
                    continue
    def dealJson(self, content, n):
        reslut = self.pipline.deal_json_eachProvs(content, n)
        if reslut:
            self.spyder.get_data_from_scence_Json(content)
        return reslut #这个不能少啊

    '''-----------------分割线--------------'''
    def run_sight(self):
        return self.getScenceList()

    def getScenceList(self):
        sl = self.pipline.get_Scence_list()
        for i in range(len(sl)):
            print(i)
            self.deal_the_sight(sl[i])

    def deal_the_sight(self, sg):
        sdict = self.pipline.deal_each_scence(sg)
        return self.get_sight_html(sdict)
    def get_sight_html(self, sdict):
        result = self.session.get_sight_html_qunar(sdict)
        if result:
            return self.get_sight_data(result)

    def get_sight_data(self, response):
        try:
            self.spyder.get_data_from_sight_html(response)
        except Exception as e:
            print(e)

    '''----------------分割线-------------------'''
    #获取每个景点的评论
    def run_comment(self):
        return  self.get_Scence_id()

    def get_Scence_id(self):
        sl = self.pipline.get_Scence_list()
        for i in range(len(sl)):
            print(i)
            self.deal_the_comment(sl[i])

    def deal_the_comment(self, sg):
        sdict = self.pipline.deal_each_scence(sg)
        return self.get_comment_html(sdict)

    def get_comment_html(self, sdict):
        #这里是个循环
        n = 1
        while True:
            result = self.session.get_comment_from_qunar(sdict, n)
            if result:
                check = self.pipline.deal_json_eachScence(result, n)
                if check:
                    self.get_comment_data_from_json(result)
                    n += 1
                else:
                    break
            else:
                n += 1
                continue
            break
    def get_comment_data_from_json(self, response):
        self.spyder.get_data_from_json(response)

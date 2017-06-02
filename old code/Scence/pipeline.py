# coding=utf8

'''作为数据处理的'''
import json
import os

class qunar_pipline():
    #验证景区json数据
    def deal_json_eachProvs(self, content, n):
        jsDict = json.loads(content)["data"]["totalCount"]
        t = jsDict/15
        if t> int(jsDict/15):
            t = int(jsDict/15) + 1
        if n < t:
            return True
        else:
            return False


    #处理景区json提取后的数据
    def deal_data_as_scence_list(self, dict):
        '''
         提取的内容有,名字,区域,地址,星级,简介,门票，坐标,分类,id
        '''
        #地址
        if "address" in dict.keys():
            address = dict["address"]
        else:
            address = ''
        #区域
        if "districts" in dict.keys():
            districts = dict["districts"]
        else:
            districts = ''
        #简介
        if "intro" in dict.keys():
            intro = dict["intro"].replace('\n', '')
        else:
            intro = ''
        #门票
        if "marketPrice" in dict.keys():
            marketPrice = dict["marketPrice"]
        else:
            marketPrice = ''
        #坐标
        if "point" in dict.keys():
            point = dict["point"]
        else:
            point = ''
        #分类
        if "sightCategory" in dict.keys():
            sightCategory = dict["sightCategory"]
        else:
            sightCategory = ''
        #景区id
        if "sightId" in dict.keys():
            sightId = dict["sightId"]
        else:
            sightId = ''
        #景区名字
        if "sightName" in dict.keys():
            sightName = dict["sightName"]
        else:
            sightName = ''
        #星级
        if "star" in dict.keys():
            star = dict["star"]
        else:
            star = ''
        text = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % (sightName, '\u0001', sightId, '\u0001', districts, '\u0001',
                                                         address, '\u0001', star, '\u0001', marketPrice, '\u0001',
                                                         sightCategory, '\u0001', point, '\u0001', intro, '\u0001')
        # print(text)
        self.save_as_scenceList(text)
    #数据保存
    def save_as_scenceList(self, text):
        with open(os.path.join(os.path.abspath('Data'), 'ScenceList.txt'), 'a', encoding='utf8') as f:
            f.writelines(text + '\n')

    #获取列表
    def get_Scence_list(self):
        return open(os.path.join(os.path.abspath('Data'), 'ScenceList.txt'), 'r', encoding='utf8').readlines()

    #处理每个景点数据
    def deal_each_scence(self, sg):
        sdict = {}
        sgl = sg.split('\u0001')
        sdict['id'] = sgl[1]
        sdict['name'] = sgl[0]
        return sdict
    #处理景点的数据
    def deal_data_as_sight_info(self, info):
        name = info["name"]
        star = info["star"]
        describe = info["describe"]
        loc = info["loc"]
        intro = info["intro"]
        optime = info["optime"].replace('\r\n', '').replace(' ', '')
        price = info["price"].replace('\r\n', '').replace(' ', '').replace('¥', '')
        tese = info["tese"].replace('\n', ',')
        ruyuan = info["ruyuan"]
        tips = info["tips"].replace('\t', '')
        traffic = info["traffic"]
        text = '%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s' \
               %(name, '\u0001',loc, '\u0001',star, '\u0001',describe, '\u0001', optime, '\u0001', price, '\u0001',
                 tese, '\u0001',ruyuan, '\u0001',tips, '\u0001',traffic, '\u0001',intro, '\u0001')
        self.save_as_sight_info(text)
    def save_as_sight_info(self, text):
        with open(os.path.join(os.path.abspath("Data"), 'sight_info.txt'), 'a', encoding='utf-8') as f:
            f.writelines(text + '\n')
    '''-------------------------------------------------'''
    def deal_json_eachScence(self, content, n):
        jsDict = json.loads(content)["data"]["tagList"][0]["tagNum"]
        t = jsDict / 1000
        if t > int(jsDict / 1000):
            t = int(jsDict / 1000) + 1
        if n < t:
            return True
        else:
            return False

    def deal_data_as_scence_comment(self, info):
        author = info["author"]
        content = info["content"].replace('/n', '')
        date = info['date']
        score = info['score']
        text = author + '\u0001' + date + '\u0001' + score + '\u0001' + content + '\u0001'
        self.save_as_comment(text)

    def save_as_comment(self, text):
        with open(os.path.join(os.path.abspath('Data'), 'Scence_comment_qunar.txt'), 'a', encoding='utf8') as f:
            f.writelines(text + '\n')

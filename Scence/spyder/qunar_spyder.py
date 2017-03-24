# coding=utf8

import json
from lxml import etree
from Scence.pipeline import qunar_pipline

class qunarSpyder():
    def __init__(self):
        self.pipline = qunar_pipline()
    #景区的json列表
    def get_data_from_scence_Json(self, content):
        jsDict = json.loads(content)["data"]["sightList"]
        info = {}
        for each in jsDict:
            self.pipline.deal_data_as_scence_list(each)

    #景区的数据
    def get_data_from_sight_html(self, response):
        selector = etree.HTML(response)
        info = {}
        #景区名字
        info["name"] = selector.xpath('//div[@class="mp-description-view"]/span[1]/text()')[0]
        #景区星级
        if selector.xpath('//div[@class="mp-description-view"]/span[2]'):
            info["star"] = selector.xpath('//div[@class="mp-description-view"]/span[2]/text()')[0]
        else:
            info["star"] = ''
        #景区一句话描述
        if selector.xpath('//div[@class="mp-description-onesentence"]/text()'):
            info["describe"] = selector.xpath('//div[@class="mp-description-onesentence"]/text()')[0]
        else:
            info["describe"] = ''
        # 景区位置
        if selector.xpath('//div[@class="mp-description-location"]/span[3]/text()'):
            info["loc"] = selector.xpath('//div[@class="mp-description-location"]/span[3]/text()')[0]
        else:
            info["loc"] = ''
        # 景区简介
        if selector.xpath('//div[@class="mp-charact-intro"]/div/p/text()'):
            info["intro"] = selector.xpath('//div[@class="mp-charact-intro"]/div/p/text()')[0]
        else:
            info["intro"] = ''
        # 景区开放时间
        if selector.xpath('//div[@class="mp-charact-time"]/div/div[2]/p/text()'):
            info["optime"] = selector.xpath('//div[@class="mp-charact-time"]/div/div[2]/p') \
                    [0].xpath('string(.)')
        else:
            info["optime"] = ''
        # 景区门票
        if selector.xpath('//div[@class="mp-description-price"]/span/text()'):
            info["price"] = selector.xpath('//div[@class="mp-description-price"]/span')[0].xpath('string(.)')
        else:
            info["price"] = ''
        # 景区特色
        if selector.xpath('//div[@class="mp-charact-event"]'):
            tese = ''
            for each1 in selector.xpath('//div[@class="mp-charact-event"]'):
                if each1.xpath('div/div[2]/h3/text()'):
                    tese += each1.xpath('div/div[2]/h3/text()')[0] + ','
                # 特色说明
                if each1.xpath('div/div[2]/p/text()'):
                    tese += each1.xpath('div/div[2]/p/text()')[0] + ';'
                # 景点照片
                # if each1.xpath('div/img'):
                #     img = each1.xpath('div/img/@src')[0]
                    # 保存图片
                    # self.save_pic(img, tese_name)

            info["tese"] = tese
        else:
            info["tese"] = ''
        # 其余信息
        if selector.xpath('//div[@class="mp-charact-littletips"][1]'):
            ruyuan = '入园公告 :'
            ry = selector.xpath('//div[@class="mp-charact-littletips"][1]/div/div[@class="mp-littletips-item"]')
            for each2 in ry:
                s1 = each2.xpath('div[1]/text()')[0]
                s2 = each2.xpath('div[2]')[0].xpath('string(.)').replace('\r\n', '').replace(' ', '')
                ruyuan += s1 + ':' + s2
            info["ruyuan"] = ruyuan
        else:
            info["ruyuan"] = ''
        if selector.xpath('//div[@class="mp-charact-littletips"][2]'):
            tips = '小贴士 :'
            tip = selector.xpath('//div[@class="mp-charact-littletips"][2]/div/div[@class="mp-littletips-item"]')
            for each3 in tip:
                d1 = each3.xpath('div[1]/text()')[0]
                d2 = each3.xpath('div[2]')[0].xpath('string(.)').replace('\r\n', '').replace(' ', '')
                tips += d1 + ':' + d2
            info["tips"] = tips
        else:
            info["tips"] = ''
        #交通信息
        if selector.xpath('//div[@class="mp-traffic-transfer"]/div'):
            n = 1
            traffic = ''
            while (True):
                if selector.xpath('//div[@class="mp-traffic-transfer"]/div[' + str(n) + ']'):
                    title = selector.xpath('//div[@class="mp-traffic-transfer"]/div[' + str(n) + ']/text()')[0]. \
                        replace('\n', '').replace('\r', '').replace(' ', '')
                    fangshi = selector.xpath('//div[@class="mp-traffic-transfer"]/div[' + str(n + 1) + ']')[0] \
                        .xpath('string(.)').replace('\n', '').replace('\r', '').replace(' ', '')
                    traffic += title + ': ' + fangshi + ';'
                else:
                    break
                n += 2
            info["traffic"] = traffic
        else:
            info["traffic"] = ''
        #数据提交给pipeline
        self.pipline.deal_data_as_sight_info(info)

    '''----------------------------------分割线-------------------------------'''
    def get_data_from_json(self, response):
        jsDict = json.loads(response)["data"]["commentList"]
        info = {}
        for each in jsDict:
            self.pipline.deal_data_as_scence_comment(each)



# coding=utf8
import json, os, time
import constructs
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
        elif recomend ==2:
            recomend = '差评'
        roomTypeName = info["roomTypeName"].replace('\n', '')
        createTimeString = info["createTimeString"].replace('\n', '')
        text = '%s%s%s%s%s%s%s%s%s%s%s%s' %(hid, '\u0001', nickName, '\u0001', content, '\u0001', recomend, '\u0001',
                                            roomTypeName, '\u0001', createTimeString, '\u0001')
        constructs.deal_queue(text)
    def save_as_comments(self, text, HDFS):
        #保存数据
        #一份保存在hdfs上
        with HDFS.open("/user/cloudera/tmp/trave_hotel/elong_comment.txt",'ab', replication=0) as f:
            f.write(text + '\n')

        #一份保存在本地
        with open(os.path.join(os.path.abspath("Data"), 'elong-comment.txt'), 'a', encoding='utf8') as f:
            f.write(text + '\n')

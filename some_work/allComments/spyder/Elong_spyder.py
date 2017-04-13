# coding=utf8

import json
from piplines import Elong_pipeline
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

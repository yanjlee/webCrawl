# coding=utf8

import base64
import requests
import time
import re
import json
import rsa
import binascii

class WeiBoSetting:
    # 登陆和预登录通用的请求头
    HEADERS = {
        'Host': 'login.sina.com.cn',
        'Referer': 'http://weibo.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    # 预登录和登陆时所需的URL
    PRE_LOGIN_URL = 'https://login.sina.com.cn/sso/prelogin.php'
    LOGIN_URL = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    # 时间戳
    TM = int(time.time() * 1000)
    # 表格
    PRE_LOGIN_PARAMS = {
        'entry': 'weibo',
        'callback': 'sinaSSOController.preloginCallBack',
        'rsakt': 'mod',
        'checkpin': '1',
        'client': 'ssologin.js(v1.4.18)',
    }

    DATA = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'useticket': 1,
        'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
        'vsnf': 1,
        # 'su': su,,
        'service': 'miniblog',
        # 'servertime': servertime,
        # 'nonce': nonce,
        'pwencode': 'rsa2',
        # 'rsakv': rsakv,
        # 'sp': passwd,
        'sr': '1920*1080',
        'encoding': 'UTF-8',
        'prelt': 65,
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

class WeiBoLogin:
    def __init__(self):
        self.session = requests.session()

    def execute(self, username, passwd):
        su = self.transform_su(username)
        pre_result = self.pre_login(su)
        cakes = self.deal_pre_login_info(pre_result)
        sp = self.transfrom_sp(passwd, cakes)
        login_response = self.log_in_weibo(su, sp, cakes)
        return login_response.cookies

    def transform_su(self, username):
        """这里可以添加一个部分来识别是邮箱还是手机号"""
        su = base64.b64encode(username.replace('@', '%40').encode()).decode('utf8')
        return su

    def pre_login(self, su):
        headers = WeiBoSetting.HEADERS
        params = WeiBoSetting.PRE_LOGIN_PARAMS
        params['su'] = su
        params["_"] = WeiBoSetting.TM
        response = self.session.get(WeiBoSetting.PRE_LOGIN_URL, headers=headers, params=params).content.decode('utf8')
        return response

    def deal_pre_login_info(self, info):
        js_content = re.findall('\((.*)\)', info, re.S)[0]
        js_dict = json.loads(js_content)
        cakes = {}
        # retcode = js_dict['retcode']
        cakes["servertime"] = js_dict['servertime']
        # pcid = js_dict['pcid']
        cakes["nonce"] = js_dict['nonce']
        cakes["pubkey"] = js_dict['pubkey']
        cakes["rsakv"] = js_dict['rsakv']
        # is_openlock = js_dict['is_openlock']
        # showpin = js_dict['showpin']
        # exectime = js_dict['exectime']
        return cakes

    def transfrom_sp(self, passwd, cakes):
        pk = int(cakes["pubkey"], 16)                   #讲16进制的pubkey转化成10进制
        code = int("10001", 16)
        key = rsa.PublicKey(pk, code)
        message = '\t'.join([str(cakes["servertime"]), str(cakes["nonce"])]) + '\n' + passwd
        sp = rsa.encrypt(message.encode(), key)     #加密
        sp = binascii.b2a_hex(sp).decode()  #转换为16进制
        return sp

    def log_in_weibo(self, su, sp, cakes):
        data = WeiBoSetting.DATA
        data['su'] = su
        data['sp'] = sp
        data['servertime'] = cakes['servertime']
        data['nonce'] = cakes['nonce']
        data['rsakv'] = cakes['rsakv']
        headers = WeiBoSetting.HEADERS
        responses = self.session.post(WeiBoSetting.LOGIN_URL, headers=headers, data=data)
        return responses

class WeiBoEngine:
    """
    这里就作为工程化的部分，接收cookies，session里带上cookie，然后开始去抓取数据
    这里是一个单例化的脚本，就取消了schedule模块
    """
    def __init__(self, cookie):
        self.session = requests.session()
        self.session.cookies.update(cookie)

    def modify_is_login(self):
        url = 'http://weibo.com/p/1005051604326364/home?from=page_100505&mod=TAB&is_all=1#place'
        res = self.session.get(url, headers=WeiBoSetting.HEADERS).content.decode('utf8')
        print(res)
class WeiBoDownloader:
    pass
class WeiBoSpyder:
    pass
class WeiBoPipeline:
    pass

if __name__ == '__main__':
    wbl = WeiBoLogin()
    print('开始登陆.....')
    username = input('\t\t用户名:')
    passwd = input('\t\t密码:')
    cookies = wbl.execute(username, passwd)

    t = WeiBoEngine(cookies)
    t.modify_is_login()
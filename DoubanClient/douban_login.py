# -*- coding:utf8 -*-


'''
仅仅是一个豆瓣需要验证和无验证的登录过程，并没有做产生登录错的的验证
用的HTMLParser 没有用 xpath来解析captcha
'''


import requests
from HTMLParser import HTMLParser

class doubanClinet():
    def __init__(self):
        object.__init__(self)
        self.data = {
            'source': 'None',
            'redir': 'https://www.douban.com',
            'login': '登录'
        }
        self.headers = {
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
            'origin': 'http://www.douban.com'
        }
        self.url = 'http://www.douban.com/login'
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def setupsession(self):
        r = self.session.get(self.url,headers=self.headers)
        return self.do_check(r.content)

    def login_without_captcha(self, n):
        self.data['form_email'] = raw_input('input your user name:')
        self.data['form_password'] = raw_input('input your password:')
        headers = {
            'Host': 'www.douban.com',
            'referer': 'http://www.douban.com/accounts/login?source=main'
        }
        r = self.session.post(self.url, data=self.data, headers=headers)
        print '登录成功'
        print r.content

    def login_with_captcha(self, n, captcha_id, captcha_url):
        self.data['form_email'] = raw_input('input your user name:')
        self.data['form_password'] = raw_input('input your password:')
        self.data['captcha-id'] = captcha_id
        self.data['captcha-solution'] = raw_input('please input the captcha code:[%s]:'%captcha_url)
        headers = {
            'Host': 'www.douban.com',
            'referer': 'http://www.douban.com/accounts/login?source=main'
        }
        r = self.session.post(self.url, data=self.data, headers=headers)
        print '登录成功'



    #验证登录是否需要验证码
    def do_check(self,content):
        p = find_chaptcha()
        p.feed(content)
        n = p.isChahere
        captcha_id = p.captchaValue
        captcha_url = p.captchaUrl
        print n, captcha_url, captcha_id
        if n == 1:
            print 'no captcha ,loading...'
            self.login_without_captcha(self,n)
        elif n == 0:
            print 'need captcha ,loading...'
            self.login_with_captcha(n, captcha_id, captcha_url)


def _attr(attrlist, attrname):
    for attr in attrlist:
        if attr[0] == attrname:
            return attr[1]
    return None

class find_chaptcha(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.isChahere = 1
        self.captchaUrl = None
        self.captchaValue = None

    def handle_starttag(self, tag, attrs):
        # if tag == 'div' and _attr(attrs, 'class') == 'item item-captcha':
        #     self.isChahere = 0
        # else:
        #     self.isChahere = 1

        if tag == 'img' and _attr(attrs, 'id') == 'captcha_image':
            self.captchaUrl = _attr(attrs, 'src')
            self.isChahere = 0

        if  tag == 'input' and _attr(attrs, 'type') == 'hidden' and _attr(attrs, 'name') == 'captcha-id':
            self.captchaValue = _attr(attrs, 'value')


if __name__ == '__main__':
    d = doubanClinet()
    d.setupsession()
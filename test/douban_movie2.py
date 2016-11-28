# -*- coding:utf8 -*-
import requests
from HTMLParser import HTMLParser

class movieParser(HTMLParser):  #要声明一个类 参数用HTMLParser 就调用了
    def __init__(self):
        HTMLParser.__init__(self)
        self.movies = []
        self.in_movies = False

    def handle_starttag(self, tag, attrs):
        def dealTheTag(attrlist, attrname):
            for attr in attrlist:
               if attr[0] == attrname:
                   return attr[1]
            return  None
        if tag == 'li' and dealTheTag(attrs, 'data-title') and dealTheTag(attrs, 'data-category') == 'nowplaying':
            movie = {} #这里是一个列表
            movie['title'] = dealTheTag(attrs, 'data-title')
            movie['score'] = dealTheTag(attrs, 'data-score')
            movie['star'] = dealTheTag(attrs, 'data-star')
            movie['director'] = dealTheTag(attrs, 'data-director')
            movie['actors'] = dealTheTag(attrs, 'data-actors')
            self.movies.append(movie) #字典放入列表里
            print '%(title)s|(score)s|%(star)s|%(director)s|%(actors)s' % movie
            self.in_movies = True

        if tag == 'img' and self.in_movies:
            self.in_movies = False
            movie = self.movies[len(self.movies)-1]#这一步很漂亮
            movie['cover-url'] = dealTheTag(attrs, 'src')
            _download_poster_cover(movie)

def _download_poster_cover(movie):
    header = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    }
    url = movie['cover-url']
    print 'downloading post cover from %s'%url
    s = requests.get(url, headers=header)
    fname = url.split('/')[-1]
    with open(fname, 'wb') as f:
        f.write(s.content)
    movie['cover-file'] = fname

def doTheRequest():
    url = 'https://movie.douban.com/nowplaying/chengdu/'
    header = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
    }
    page =requests.get(url, headers=header)
    parser = movieParser() #实例化
    parser.feed(page.content)
    page.close()

if __name__ == '__main__':
    doTheRequest()
    
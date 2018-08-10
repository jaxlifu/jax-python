# -*- coding=utf-8 -*-
#!/usr/bin/env python
import os
import pickle
import re
import sys
from urllib import parse

import requests
from bs4 import BeautifulSoup

# 修改递归深度
# sys.setrecursionlimit(2**16)


class Downloader(object):
    def __init__(self, *args, **kwargs):
        self.hostUrl = 'http://m.xbiquge.cc'
        self.searchUrl = 'http://m.xbiquge.cc/modules/article/waps.php?searchtype=articlename&searchkey={0}&t_btnsearch='
        self.name, self.id = '', ''
        self.lastUrl, self.lastChaptersUrl = None, None
        self.pattern = re.compile(
            r'<|>|/|-->>|本章未完，点击下一页继续阅读|_Middle\(\);|&nbsp;|(第.*?章 .*?\s)')

    def searchBook(self, name):
        '''
        更据书籍名称搜索书籍,获取搜索的url
        '''
        self.name = name
        url = self.searchUrl.format(
            parse.quote(name.encode(encoding='gb2312')))
        self.getBookInfo(url)

    def getBookInfo(self, url):
        '''
        获取书籍基本信息
        '''
        print('正在获取书籍信息...', end='\r')
        page = requests.get(url)
        page.encoding = 'GBK'
        if page.status_code == 200:
            bs = BeautifulSoup(page.text, 'html5lib')
            chaptersUrl = bs.find_all(
                'a', href=[re.compile('chapters')])[0]['href']
            bookId = bs.find_all('a', text=['立即阅读'])[0]['href']
            bookId = re.findall(r'/(book_.*?)/', bookId)[0]
            self.id = bookId
            # 获取书籍章节目录
            chaptersUrl = '{0}{1}'.format(self.hostUrl, chaptersUrl)
            self.getBookChapters(chaptersUrl)

    def getBookChapters(self, url):
        '''
        获取目录信息
        '''
        print('正在获取目录列表...', end='\r')
        self.lastChaptersUrl = url
        page = requests.get(url)
        page.encoding = 'GBK'
        if page.status_code == 200:
            bs = BeautifulSoup(page.text, 'html5lib')
            chaptersList = bs.find_all('a', text=[re.compile(r'第*.?章')])
            # 获取章节列表
            chaptersList = ['{0}{1}'.format(
                self.hostUrl, item['href']) for item in chaptersList]
            if self.lastUrl in chaptersList:
                chaptersList = chaptersList[chaptersList.index(self.lastUrl):]
            if chaptersList:
                for item in chaptersList:
                    self.getBookDetails(item)
            # 加载下一页
            nextPage = bs.find_all('a', text=['下一页'])
            if nextPage:
                nextUrl = '{0}{1}'.format(self.hostUrl, nextPage[0]['href'])
                self.getBookChapters(nextUrl)

    def getBookDetails(self, url):
        '''
        获取章节详细内容
        '''
        page = requests.get(url)
        page.encoding = 'GBK'
        if page.status_code == 200:
            bs = BeautifulSoup(page.text, 'html5lib')
            # 获取章节标题
            title = bs.title.text
            title = re.findall(r'^(.*?)_', title)[0]
            print('正在下载{:>20s}...'.format(title), end='\r')
            # 获取章节内容
            content = bs.find_all(id='nr1')
            nextPage = bs.find_all('a', text=['下一页'])
            if content:
                content = content[0].text
                content = content.strip()
                # 去掉部分不需要的内容
                content = self.pattern.sub('', content)
            with open('{0}.txt'.format(self.name), 'a+', encoding='utf-8') as f:
                # 判断是否需要添加章节标题
                if not re.findall(r'/(\d+_\d).html', url):
                    self.lastUrl = url
                    f.write('{0}\n'.format(title))
                f.write('{0}\n\r'.format(content))

            # 是否有下一页
            if nextPage:
                nextUrl = '{0}{1}'.format(self.hostUrl, nextPage[0]['href'])
                self.getBookDetails(nextUrl)

    def saveLastInfo(self):
        '''
        保存当前下载位置
        '''
        obj = {
            'url': self.lastUrl,
            'chaptersUrl': self.lastChaptersUrl,
            'id': self.id,
            'name': self.name
        }
        f = open('download.data', 'wb')
        pickle.dump(obj, f)
        f.close()

    def loadLastInfo(self):
        '''
        获取当前下载的位置
        '''
        if os.path.exists('download.data'):
            f = open('download.data', 'rb')
            obj = pickle.load(f)
            self.id = obj['id']
            self.lastUrl = obj['url']
            self.name = obj['name']
            self.lastChaptersUrl = obj['chaptersUrl']
            f.close()

    def start(self, name):
        self.loadLastInfo()
        if self.lastUrl:
            self.getBookChapters(self.lastChaptersUrl)
        else:
            self.searchBook(name)


def main(name):
    downloader = Downloader()
    try:
        downloader.start(name)
    except BaseException as _:
        # 出现异常的时候保存当前下载进度
        downloader.saveLastInfo()
    pass


if __name__ == '__main__':
    name = input('please input book name: ')
    main(name)
    print('书籍下载完成!')

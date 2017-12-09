#!/usr/bin/env python
# coding=utf-8

import requests
import re
import os

# 测试get和post请求


def get_post_test():
    r = requests.get('https://www.bilibili.com')
    r.encoding = 'utf-8'
    print('bilibili index info is:===> \n%s' % (r.text))

    r = requests.post('http://httpbin.org/post')
    print('httpbin index info is===>\n %s' % (r.text))


def getHtmlSource():
    # f = open('zhihu-message.log', 'w')
    # for pageNum in range(1, 21):
    #     url = "http://www.zhihu.com/collection/27109279?page=%d" % (pageNum)
    #     print('zhihu-url is \n%s' % (url))
    #     r = requests.get(url)
    #     r.encoding = 'utf-8'
    #     print('zhihu-message is \n%s' % (r.text))
    # f.close()
    keyword = input("int put keyword :")
    # 创建一个关键字对应的目录
    dirPath = '%s/%s' % (os.getcwd(), keyword)
    if not os.path.exists(dirPath):
        os.mkdir(dirPath)

    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1460997499750_R&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%s' % (
        keyword)
    request = requests.get(url)
    #request.encoding = 'utf-8'
    request.encoding = 'utf-8'
    html = request.text
    print("text of images is %s \n" % (html))
    log = open('%s/web-log.html' % (keyword), 'w+', encoding='utf-8')
    log.write(html)
    log.close()
    picUrls = re.findall('"objURL":"(.*?)",', html, re.S)

    index = 0
    for picUrl in picUrls:
        print("pic url is %s \n" % (picUrl))
        try:
            img = requests.get(picUrl, timeout=10)
        except requests.exceptions.ConnectionError:
            print("image download error!")
            continue
        image = "%s/picture%d.png" % (keyword, index)
        # resolve the problem of encode, make sure that chinese name could be store
        f = open(image, 'wb')
        f.write(img.content)
        f.close
        index += 1


if __name__ == '__main__':
    getHtmlSource()

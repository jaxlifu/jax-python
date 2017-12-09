#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import re
import os
'''
**第 0013 题：** 用 Python 写一个爬图片的程序，爬 [这个链接里的日本妹子图片 :-)](http://tieba.baidu.com/p/2166231880)
'''

session = requests.Session()


def get_html(url='http://tieba.baidu.com/p/2166231880'):
    page = session.get(url)
    html = page.text
    '''
    #<img pic_type="0" class="BDE_Image" src="http://imgsrc.baidu.com/forum/w%3D580%3Bcp%3Dtieba%2C10%2C302%3Bap%3D%C9%BC%B1%BE%D3%D0%C3%C0%B0%C9%2C90%2C310/sign=8800a2e3b3119313c743ffb855036fa7/1e29460fd9f9d72abb1a7c3cd52a2834349bbb7e.jpg" bdwater="杉本有美吧,955,550" width="560" height="323" changedsize="true" style="cursor: url(&quot;http://tb2.bdstatic.com/tb/static-pb/img/cur_zin.cur&quot;), pointer;">
    '''
    image_list = re.findall(
        r'<img pic_type="0" class="BDE_Image" src="(.*?)"', html)

    with open('tieba.html', 'wb') as f:
        f.write(page.content)
        f.close()
    folder = 'photos'
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    for image_url in image_list:
        get_image(image_url)
    pass


def get_image(url=''):
    if not url:
        print('url is empty')
        return
    image_page = session.get(url)
    names = url.split('/')[-1]
    with open(names, 'wb') as img:
        img.write(image_page.content)
        img.close()
    pass


if __name__ == '__main__':
    get_html()

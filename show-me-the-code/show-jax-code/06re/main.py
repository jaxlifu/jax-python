#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests


def get_html():
    url = 'http://www.bilibili.com'
    page = requests.get(url)
    html = page.text
    bodys = re.findall(r'<body>(.*?)</body>', html, re.S)
    links = re.findall(r'<a(.*?)</a>', html, re.S)
    links = [('<a%s</a>' % x) for x in links]
    print(bodys, links)
    with open('bilibili.html', 'wb') as f:
        f.write(page.content)
        f.close()
    pass


if __name__ == '__main__':
    name = input('input > ')
    print(name)
    get_html()

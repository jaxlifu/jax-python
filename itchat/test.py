#!/usr/bin/env python
# -*- coding: utf-8 -*-
from baidu_img import *
import requests


if __name__ == '__main__':
    init_headers()
    result = baidu_image(
        'http://emoji.qpic.cn/wx_emoji/AnJ9zOianOexJrtlxMPfKfBstGaLsJ7GeokCClrV4u5ibs3Lbls4ichpg/')
    print(result)

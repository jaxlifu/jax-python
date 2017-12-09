#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def check_filename(filename=None):
    '''
    文件名不能包含以下字符" \/:*?"<>| ",所以用"_"替换
    for options
        - filename: 文件名如果为空则直接返回,否则替换掉文件名中的特殊字符
    '''
    if not filename:
        return
    return re.sub(r'\\|\/|\:|\*|\?|\<|\>|\|', '_', filename)
    pass


def init_header(requestHeader):
    if not requestHeader or not requestHeader.strip():
        return

    headers = {}
    cookies = {}

    lines = [line for line in requestHeader.strip().split('\n')
             if line and line.strip()]
    for line in lines:
        items = line.split(':', 1)
        if not items or len(items) < 2:
            continue
        if items[0] == 'Cookie':
            cookies = _init_cookie(items[1])
        else:
            headers[items[0]] = items[1]
    return headers, cookies
    pass


def _init_cookie(cookie):
    if not cookie:
        return

    cookie_dict = {}
    lines = cookie.split(';', 1)
    for line in lines:
        items = line.split('=', 1)
        if not items or len(items) < 2:
            continue
        cookie_dict[items[0]] = items[1]
    return cookie_dict
    pass

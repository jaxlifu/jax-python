#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import base64
import json
'''
做为 Apple Store App 独立开发者，你要搞限时促销，为你的应用**生成激活码**（或者优惠券），使用 Python 如何生成 200 个激活码（或者优惠券）？
'''


def code_generator():
    f = open('random_codes.txt', 'w')
    for i in range(0, 200):
        code = ''
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        for position in range(0, 8):
            index = random.randint(1, len(chars))  # 0-62
            code += chars[index - 1]
        # print(code)
        f.write("%s\n" % code)
    f.close()
    pass


def base64_generator():
    message = {}
    f = open('base64_code.txt', 'w')
    for i in range(0, 200):
        message['id'] = i
        message['goods'] = 'product%d' % i
        raw_64 = base64.b64encode(json.dumps(message).encode(encoding='utf_8'))
        code = raw_64.decode().replace('=', '')
        f.write('%s\n' % code[-8:])
    f.close()


if __name__ == '__main__':
    code_generator()
    base64_generator()

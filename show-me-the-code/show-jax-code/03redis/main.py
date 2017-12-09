#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import base64
import json
import re
'''
将 0001 题生成的 200 个激活码（或者优惠券）保存到 **Redis** 非关系型数据库中。 
'''


def base64_generator():
    message = {}
    codes = []
    for i in range(0, 200):
        message['id'] = i
        message['goods'] = 'product%d' % i
        raw_64 = base64.b64encode(json.dumps(message).encode(encoding='utf-8'))
        code = raw_64.decode().replace('=', '')
        codes.append(code[-8:])
    return codes


def redis_init():
    conn = redis.Redis(host='localhost', port=6379)
    return conn


def push_to_redis(key_list):
    for key in key_list:
        redis_init().lpush('message', key_list)
    pass


def get_from_redis():
    key_list = redis_init().lrange('message', 0, -1)
    print(key_list)


if __name__ == '__main__':
    codes = base64_generator()
    push_to_redis(codes)
    get_from_redis()

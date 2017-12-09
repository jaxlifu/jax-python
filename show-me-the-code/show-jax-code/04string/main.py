#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
'''
任一个英文的纯文本文件，统计其中的单词出现的个数。
'''


def word_count():
    words = []  # 从文件中获取的单词列表
    repeats = {}  # 获取单词的重复次数
    with open('README.md', mode='r') as readme:
        data = readme.read()
        # words = data.split(r'[^a-zA-Z]')
        words = re.split(r'[^a-zA-Z]', data)
        words = [x for x in words if x != '']
        readme.close()
    for word in words:
        if word in repeats:
            repeats[word] += 1
        else:
            repeats[word] = 1
    return repeats
    pass


def primary_word(maps={}):
    count = max(maps.values())  # 获取出现最多的次数
    # 获取出现最多次数的单词,可能有多个单词出现的次数一样
    word = [key for key in maps if maps[key] == count]
    return (word, count)

    pass


if __name__ == '__main__':
    repeats = word_count()
    print(primary_word(repeats))

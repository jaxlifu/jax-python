#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
'''
**第 0011 题：** 敏感词文本文件 filtered_words.txt，里面的内容为以下内容，当用户输入敏感词语时，则打印出 Freedom，否则打印出 Human Rights。

    北京
    程序员
    公务员
    领导
    牛比
    牛逼
    你娘
    你妈
    love
    sex
	jiangge

**第 0012 题：** 敏感词文本文件 filtered_words.txt，里面的内容 和 0011题一样，当用户输入敏感词语，则用 星号 * 替换，例如当用户输入「北京是个好城市」，则变成「**是个好城市」。
'''


def read_file():
    data = ''
    with open('filtered_words.txt', 'r') as f:
        data = f.readlines()
        f.close()
    return data
    pass


if __name__ == '__main__':
    try:
        message = input('input > ')
        for word in read_file():
            word = word.strip()
            if message.find(word) != -1:
                print(message.replace(word, len(word) * '*'))
    except Exception as e:
        print(e)

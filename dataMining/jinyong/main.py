#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import re
import sys

import gensim
import jieba
import jieba.posseg as pseg
import matplotlib.pyplot as pyplot
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

jieba.set_dictionary('dict.txt')

NOVELS_DIR = 'novels'
novels_list = os.listdir(NOVELS_DIR)


def load_names():
    names = {}
    for novels in novels_list:
        novels_name = novels.split('.')[0]
        people_names = {}
        with open('%s/%s' % (NOVELS_DIR, novels), 'r', encoding='GBK') as f:
            for line in f.readlines():
                poss = pseg.cut(line)
                for w in poss:
                    if w.flag != 'nr' or len(w.word) < 2:
                        continue

                    if w.word in people_names:
                        people_names[w.word] += 1
                    else:
                        people_names[w.word] = 1
        names[novels_name] = people_names


    with open('names.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(names, ensure_ascii=False))

    pass


def find_main_charecters(novel, num=10):
    """
    docstring here
        :param novel: 
        :param num=10: 
    """
    pass


def make_userdict():
    '''
    将存储的姓名的文本转化为jieba能使用的字典
    '''
    with open('jinyong_names.txt', 'r', encoding='GBK') as f:
        lines = [line.strip() for line in f.readlines()
                 if line.strip() and not '人物' in line]
    with open('dict.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.writelines(fromat_line_name('%s\n' % line))
    pass


def fromat_line_name(msg):
    return re.sub(r'\s+', ' 100 nr\n', format_brocket_name(msg))
    pass


def format_brocket_name(msg):
    """
    docstring here
        :param msg: 
    """
    return re.sub(r'[\(.*?\)]', ' ', msg)
    pass


if __name__ == '__main__':
    load_names()
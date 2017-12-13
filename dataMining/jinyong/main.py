#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np
import matplotlib.pyplot as pyplot
import pandas as pd
from pandas import Series, DataFrame
import gensim
import jieba
import jieba.posseg as pseg
import json

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
                        people_names[w.word] = 0
        names[novels_name] = people_names

    with open('names.txt', 'w', encoding='utf-8') as f:
        f.write(json.dumps(names, ensure_ascii=False))

    pass

def find_main_charecters(novel,num=10):

    pass


if __name__ == '__main__':
    # load_names()

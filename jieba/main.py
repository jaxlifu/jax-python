#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import jieba
import codecs
import math
from jieba.posseg import cut


names = {}
relationships = {}
lineNames = []


def load_userdict():
    jieba.load_userdict('dict.txt')
    with open('busan.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            poss = cut(line)
            for w in poss:
                if w.flag != 'nr' or len(w.word) < 2:
                    continue
                if not w.word in lineNames:
                    lineNames.append(w.word)
                    names[w.word] = 1
                    relationships[w.word] = {}
                else:
                    names[w.word] += 1
    pass

def fun_relationships():
    for line in lineNames:
        print(line)
    pass



if __name__ == '__main__':
    load_userdict()
    fun_relationships()

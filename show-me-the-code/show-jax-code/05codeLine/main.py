#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import re
'''
有个目录，里面是你自己写过的程序，统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。
'''


def scanf_folders(parent='java'):
    for filename in os.listdir(parent):
        child = os.path.join(parent, filename)
        if os.path.isdir(child):
            scanf_folders(child)
        else:
            # print(child)
            read_file(child)
            break
    pass


def read_file(path):
    annotation_count = 0
    code_count = 0
    blank_count = 0
    with open(path, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        # java 注释 // /* */ * 开头的
        # python 注释是以 # 开头 但是
        # 多行注释 '''\n\n\n''' 或"""\n\n\n"""不适合以行的方式来读取
        for line in lines:
            line = line.strip()
            if not line:
                blank_count += 1
            elif line.startswith('//') or line.startswith('/*') or line.startswith('*/') or line.startswith('*'):
                annotation_count += 1
            else:
                code_count += 1

    print(path,
          'total line %d' % len(lines),
          'annotation line %d' % annotation_count,
          'code line %d' % code_count,
          'black line %d' % blank_count)
    pass


if __name__ == '__main__':
    scanf_folders()

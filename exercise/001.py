#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 题目：有1、2、3、4个数字，能组成多少个互不相同且无重复数字的三位数？都是多少？

for i in range(1, 5):  # 百位
    for j in range(1, 5):  # 十位
        for k in range(1, 5):  # 个位
            if i == j or i == k or j == k:
                continue
            print(i * 100 + j * 10 + k)

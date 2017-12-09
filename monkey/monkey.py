#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys


def monkey():
    for index in range(100):
        os.system('adb shell monkey -v -v -v 10000 > E:\log\monkey%d.log' % index)
    pass


if __name__ == '__main__':
    monkey()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlwt


def read_file(name='numbers.txt'):
    data = ''
    with open(name, mode='r') as f:
        data = f.read()
        f.close()
    return data
    pass


def generate_xls(data=''):
    _numbers = eval(data)
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('numbers')
    row, column = 0, 0
    for items in _numbers:
        column = 0
        for item in items:
            worksheet.write(row, column, item)
            column += 1
        row += 1
    workbook.save('numbers.xls')
    pass


if __name__ == '__main__':
    generate_xls(data=read_file())

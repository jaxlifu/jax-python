#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xlwt


def read_file(name='city.txt'):
    data = ''
    with open(name, mode='r') as f:
        data = f.read()
        f.close()
    return data
    pass


def generate_xls(data=''):
    city = eval(data)
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('city')
    row = 0
    for key in city:
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, city[key])
        row += 1
    workbook.save('city.xls')
    pass


if __name__ == '__main__':
    generate_xls(data=read_file())

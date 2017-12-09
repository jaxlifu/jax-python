#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import xlwt

'''
**第 0014 题：** 纯文本文件 student.txt为学生信息, 里面的内容（包括花括号）如下所示：

    {
    	"1":["张三",150,120,100],
    	"2":["李四",90,99,95],
    	"3":["王五",60,66,68]
    }

请将上述内容写到 student.xls 文件中，如下图所示：
'''


def read_file():
    data = ''
    with open('student.txt', 'r') as f:
        data = f.read()
        f.close()
    return data
    pass


def generate_xls(data=''):
    student = eval(data)
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('student')
    worksheet.write(0, 0, '姓名')
    worksheet.write(0, 1, '语文')
    worksheet.write(0, 2, '数学')
    worksheet.write(0, 3, '英语')
    row, column = (1, 0)
    for key in student:
        values = student[key]
        column = 0
        for value in values:
            worksheet.write(row, column, value)
            column += 1
        row += 1
    workbook.save('student.xls')
    pass


if __name__ == '__main__':
    data = read_file()
    generate_xls(data=data)

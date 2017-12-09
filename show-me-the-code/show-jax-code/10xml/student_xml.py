#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import json
from xml.dom.minidom import Document

'''
将 第 0014 题中的 student.xls 文件中的内容写到 student.xml 文件中，如

下所示：

    <?xml version="1.0" encoding="UTF-8"?>
    <root>
    <students>
    <!--
    	学生信息表
    	"id" : [名字, 数学, 语文, 英文]
    -->
    {
    	"1" : ["张三", 150, 120, 100],
    	"2" : ["李四", 90, 99, 95],
    	"3" : ["王五", 60, 66, 68]
    }
    </students>
    </root>
'''


def read_xls(filename='student.xls'):
    data = {}
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    rows, cols = (worksheet.nrows, worksheet.ncols)
    for row in range(rows):
        item_list = []
        key = worksheet.cell_value(row, 0)
        for col in range(1, cols):
            item_list.append(worksheet.cell_value(row, col))
        data[key] = item_list
    return data
    pass


def write_xml(filename='student.xml', data={}):
    doc = Document()
    root = doc.createElement('root')
    doc.appendChild(root)

    students = doc.createElement('student')
    students.appendChild(doc.createComment('''学生信息表
    "id" : [名字, 数学, 语文, 英文]'''))
    students.appendChild(doc.createTextNode(
        json.dumps(data, ensure_ascii=False)))
    root.appendChild(students)
    with open(filename, 'w') as f:
        doc.writexml(f, indent="\t", newl="\n", encoding='utf-8')
    pass


if __name__ == '__main__':
    data = read_xls()
    print(data)
    write_xml(data=data)

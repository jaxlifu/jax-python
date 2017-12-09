#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
from xml.dom.minidom import Document
import json
'''
将 第 0016 题中的 numbers.xls 文件中的内容写到 numbers.xml 文件中，如下

所示：

    <?xml version="1.0" encoding="UTF-8"?>
    <root>
    <numbers>
    <!--
    	数字信息
    -->

    [
    	[1, 82, 65535],
    	[20, 90, 13],
    	[26, 809, 1024]
    ]

    </numbers>
    </root>
'''


def read_xls(filename='numbers.xls'):
    data = []

    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    rows, cols = (worksheet.nrows, worksheet.ncols)
    for row in range(rows):
        item_list = []
        for col in range(cols):
            item_list.append(worksheet.cell_value(row, col))
        data.append(item_list)
    return data
    pass


def write_xml(filename='numbers.xml', data=[]):
    doc = Document()

    root = doc.createElement('root')
    doc.appendChild(root)

    numbers = doc.createElement('numbers')
    numbers.appendChild(doc.createComment('数字信息'))
    numbers.appendChild(doc.createTextNode(
        json.dumps(data, ensure_ascii=False)))
    root.appendChild(numbers)
    with open(filename, 'w') as f:
        doc.writexml(f, indent="\t", newl="\n", encoding='utf-8')
    pass


if __name__ == '__main__':
    data = read_xls()
    print(data)
    write_xml(data=data)

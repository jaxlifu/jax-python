#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import json
from xml.dom.minidom import Document
'''
 将 第 0015 题中的 city.xls 文件中的内容写到 city.xml 文件中，如下所示：

    <?xmlversion="1.0" encoding="UTF-8"?>
    <root>
    <citys>
    <!--
    	城市信息
    -->
    {
    	"1" : "上海",
    	"2" : "北京",
    	"3" : "成都"
    }
    </citys>
    </root>

'''


def read_xls(name='city.xls'):
    # 获取xls文件excel的book对象
    workbook = xlrd.open_workbook(name)
    # 获取sheet对象
    sheet_name = workbook.sheet_names()[0]
    worksheet = workbook.sheet_by_name(sheet_name)
    # worksheet = workbook.sheet_by_index(0)
    # 获取行和列
    workrows = worksheet.nrows
    workcols = worksheet.ncols
    citys = {}
    for row in range(workrows):
        key = worksheet.cell_value(row, 0)
        value = worksheet.cell_value(row, 1)
        citys[key] = value
    return citys
    pass


'''
<?xmlversion="1.0" encoding="UTF-8"?>
<root>
<citys>
<!--
    城市信息
-->
{
    "1" : "上海",
    "2" : "北京",
    "3" : "成都"
}
</citys>
</root>
'''


def write_xml(filename='city.xml', data={}):
    doc = Document()

    # 添加root节点
    root = doc.createElement('root')
    doc.appendChild(root)

    # 添加citys节点
    citys = doc.createElement('citys')

    city_annotation = doc.createComment('城市信息')
    # json中文字符不转义的方法
    city_text = doc.createTextNode(json.dumps(data, ensure_ascii=False))
    citys.appendChild(city_annotation)
    citys.appendChild(city_text)
    root.appendChild(citys)

    with open(filename, 'w') as f:
        doc.writexml(f, newl="\n", indent="\t", encoding='utf-8')
    pass


if __name__ == '__main__':
    data = read_xls()
    write_xml(data=data)

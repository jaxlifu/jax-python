#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
'''
[登陆中国联通网上营业厅](http://iservice.10010.com/index_.html)
 后选择「自助服务」 --> 「详单查询」，然后选择你要查询的时间段，点击「查询」按钮，查询结果页面的最下方，点击「导出」，
 就会生成类似于 2014年10月01日～2014年10月31日通话详单.xls 文件。写代码，对每月通话时间做个统计。
'''


def read_xls(filename='CallInfo.xls'):
    workbook = xlrd.open_workbook(filename)
    worksheet = workbook.sheet_by_index(0)
    rows, cols = (worksheet.nrows, worksheet.ncols)
    call_in = {}
    call_out = {}

    for row in range(1, rows):
        rows_list = worksheet.row(row)
        call_time = rows_list[3].value
        call_type = rows_list[4].value
        call_phone = rows_list[5].value
        if call_type == '主叫':
            if call_phone in call_out:
                call_out[call_phone] += 1
            else:
                call_out[call_phone] = 1
        elif call_type == '被叫':
            if call_phone in call_in:
                call_in[call_phone] += 1
            else:
                call_in[call_phone] = 1

    #print('call in %s\n' % call_in, 'call out %s \n' % call_out)
    max_in = max(call_in.values())
    max_in_list = [x for x in call_in.keys() if call_in[x] == max_in]
    max_out = max(call_out.values())
    max_out_list = [x for x in call_out.keys() if call_out[x] == max_out]
    print('主叫最多的手机号是%s' % max_out_list, '次数是%s' % max_out)
    print('被叫最多的手机号是%s' % max_in_list, '次数是%s' % max_in)
    pass


if __name__ == '__main__':
    read_xls()

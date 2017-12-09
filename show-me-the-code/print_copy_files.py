#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
# 在vendor/rockchip/common/media 目录下执行改文件
# 打印出需要复制到out对应目录下的文件信息
root = os.getcwd()

out_list = []


def print_file_name(parent):
    # 打印需要复制的文件信息将打印的信息添加到device-vendor.mk文件
    os.chdir(parent)
    file_list = os.listdir()
    for name in file_list:
        filePath = os.path.join(parent, name)
        if os.path.isdir(filePath):
            print_file_name(filePath)
        else:
            tempName = filePath.replace(root, '')
            message = 'vendor/rockchip/common/media%s:system/media%s \\' % (
                tempName, tempName)
            # 将要输出的内容放在列表中,方便排序
            out_list.append(message)
    pass


if __name__ == '__main__':
    print_file_name(root)
    out_list.sort()
    for item in out_list:
        if '.py' in item:
            continue
        print(item)

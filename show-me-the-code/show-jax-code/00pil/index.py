#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
import json
import sys
import os
'''
将你的 QQ 头像（或者微博头像）右上角加上红色的数字，类似于微信未读信息数量那种提示效果。
'''

# 将图片转化为jpeg存储


def convert_jpeg():
    # sys。argv python3 index。py 0。png 1。png
    for infile in sys.argv[1:]:
        f, e = os.path.splitext(infile)
        print(infile, f, e)
        outfile = '%s.jpg' % f
        if infile != outfile:
            try:
                Image.open(infile, mode="r").save(outfile)
            except Exception as e:
                print(e)
    pass

# 创建缩略图


def create_thumbnails():
    size = (128, 128)  # size
    for infile in sys.argv[1:]:
        outfile = os.path.splitext(infile)[0] + '.thumbnail'
        if infile != outfile:
            try:
                img = Image.open(infile, mode="r")
                img.thumbnail(size)
                img.save(outfile, 'JPEG')
            except Exception as e:
                print('create thumbnail fail %s' % e)
    pass

# 验证是否是图片，输出图片信息


def identify_image():
    for infile in sys.argv[1:]:
        try:
            with Image.open(infile) as img:
                print(infile, infile.format, '%d * %d' % img.size, img.mode)
        except Exception as e:
            print(e)

    pass


# 旋转图片
def rolling_image(image, delta):
    xsize, ysize = image.size
    delta = delta % xsize
    if delta == 0:  # 不需要旋转
        return image

    part1 = image.crop(0, 0, delta, ysize)
    part2 = image.crop(delta, 0, xsize, ysize)
    part1.load()
    part2.load()
    image.paste(part2, (0, 0, xsize - delta, ysize))
    image.pastet(part1, (xsize - delta, 0, xsize, ysize))
    return image
    pass

#在图片上添加文字
def add_text():
    try：
        img = Image.open('picture0.png')
        xy = (img.size[0] - 400, 100)
        draw = ImageDraw.Draw(img)
        # 不知道有没有不设置字体直接设置文字大小的方法
        font = ImageFont.truetype(font='msyh.ttf', size=50)
        # 网上说的中文的问题暂时没有遇到
        draw.text(xy, '我是小埋', fill=(255, 10, 10), font=font)
        img.save('pic_number.png')
    except Exception as e：
        print('error with %s' % e)
    pass


if __name__ == '__main__':
    add_text()
    # convert_jpeg()
    # create_thumbnails()
    # identify_image()

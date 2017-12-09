#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageFont, ImageDraw
import random
import string


def generate_captcha():
    return random.choice(string.ascii_letters + string.digits)
    pass


def random_bg_color():
    r = random.randint(64, 255)
    g = random.randint(64, 255)
    b = random.randint(64, 255)
    return (r, g, b)


def random_font_color():
    r = random.randint(32, 127)
    g = random.randint(32, 127)
    b = random.randint(32, 127)
    return (r, g, b)


def generate_image():
    # 创建一个图片
    size = (60 * 4, 60)
    img = Image.new('RGB', size, color=(255, 255, 255))
    font = ImageFont.truetype(font='msyh.ttf', size=36)
    draw = ImageDraw.Draw(img)
    for i in range(size[0]):
        for j in range(size[1]):
            draw.point((i, j), fill=random_bg_color())
    for i in range(4):
        x, y = (random.randint(0, 60) + i * 50, random.randint(0, 10))
        draw.text((x, y), generate_captcha(), random_font_color(), font)
    img.save('captcha.png', format='PNG')
    img.close()
    pass


if __name__ == '__main__':
    generate_image()

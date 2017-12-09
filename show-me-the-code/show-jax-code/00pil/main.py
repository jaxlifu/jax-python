#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from PIL import Image


def process_image(filename, width=640, height=1136):
    try:
        img = Image.open(os.path.join('photos', filename), mode="r")
        w, h = img.size
        scale = 1.0
        if w <= width and h < height:
            # 默认就符合分辨率
            return
        if float(w) / width > float(h) / height:
            scale = float(w) / width
        else:
            scale = float(h) / height

        img_new = img.resize((int(w / scale), int(h / scale)), Image.ANTIALIAS)
        img_new.save(os.path.join('photos', 'new_%s' % filename))
        img_new.close()
    except Exception as e:
        print(e)

    pass


if __name__ == '__main__':
    photos = os.listdir('photos')
    for filename in photos:
        process_image(filename)

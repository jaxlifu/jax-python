#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

with open('header.txt') as f:
    text = f.read()
    alice_coloring = np.array(Image.open('sphx_glr_colored_003.png'))
    stopwords = set(STOPWORDS)
    stopwords.add('said')

    wc = WordCloud(background_color='white', max_words=2000,
                   mask=alice_coloring, stopwords=stopwords,
                   max_font_size=40, random_state=42)
    wc.generate(text)

    image_color = ImageColorGenerator(alice_coloring)

    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.figure()

    plt.imshow(wc.recolor(color_func=image_color), interpolation='bilinear')
    plt.axis('off')
    plt.figure()
    plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis('off')
    plt.show()

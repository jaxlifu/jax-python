#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('header.txt') as f:
    text = f.read()
    wc = WordCloud().generate(text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    wc = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.show()

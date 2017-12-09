#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

with open('header.txt') as f:
    text = f.read()
alice_mask = np.array(Image.open('sphx_glr_masked_002.png'))

stopwords = set(STOPWORDS)
stopwords.add('said')

wc = WordCloud(background_color='white', max_words=2000, mask=alice_mask,
               stopwords=stopwords)
wc.generate(text)
wc.to_file('alice.png')

plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.figure()
plt.imshow(alice_mask,cmap=plt.cm.gray,interpolation='bilinear')
plt.axis('off')
plt.show()

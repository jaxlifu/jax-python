#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import pandas
from wordcloud import WordCloud

logging.basicConfig(level=logging.DEBUG)


def read_friend_list():
    with open('friend.json', 'r', encoding='utf-8') as f:
        friend_list = eval(f.read())
    return friend_list
    pass


def analyzes_sex(friends):
    male, female, others = (0, 0, 0)
    for friend in friends:
        sex = friend['Sex']
        if sex == 1:  # male
            male += 1
        elif sex == 2:
            female += 1
        else:
            others += 1
    index = np.arange(3)
    genders = (male, female, others)
    bar_width = 0.35
    plt.figure(figsize=(14, 7))
    plt.bar(index, genders, bar_width, alpha=0.6, color='rgb')
    plt.xlabel('gender', fontsize=16)
    plt.ylabel('population', fontsize=16)
    plt.title('Male-Female population', fontsize=16)
    plt.xticks(index, ('Male', 'Female', 'Others'), fontsize=14, rotation=20)
    plt.ylim(0, 220)
    for index, gender in zip(index, genders):
        plt.text(index, gender + 0.1, "%.0f" % gender, ha='center',
                 va='bottom', fontsize=14, color='black')
    plt.show()
    # plt.imsave('sex.png')

    pass


def analyzes_info(friends):
    info_list = [{
        'Province': item['Province'],
        'NickName':item['NickName'],
        'RemarkName':item['RemarkName'],
        'Signature':item['Signature'],
        'Sex':item['Sex'],
        'City':item['City']
    } for item in friends]
    features = pandas.DataFrame(info_list)
    locations = features.loc[:, ['Province', 'City']]  # 获取位置信息列
    locations = locations[locations['Province'] != '']
    data = locations.groupby(['Province', 'City']).size().unstack()
    count_subset = data.take(data.sum(1).argsort())[-20:]

    subset_plot = count_subset.plot(kind='bar', stacked=True, figsize=(24, 24))
    xtick_labels = subset_plot.get_xticklabels()
    font = FontProperties(fname='simfang.ttf', size=14)
    for label in xtick_labels:
        label.set_fontproperties(font)
    legend_labels = subset_plot.legend().texts
    for label in legend_labels:
        label.set_fontproperties(font)
        label.set_fontsize(10)

    plt.xlabel('Province', fontsize=20)
    plt.xlabel('Number', fontsize=20)
    plt.show()
    # plt.imsave('location.png')
    pass


def analyzes_signature(friends):
    signature_list = [item['Signature'].strip().replace('\n', '')
                      for item in friends]
    word_list = jieba.cut(''.join(signature_list))
    words = ''.join(word_list)
    wc = WordCloud(background_color='white', max_words=2000,
                   max_font_size=60, font_path='simfang.ttf', scale=2, random_state=42)
    wc.generate(words)
    wc.to_file('signature.png')
    pass


if __name__ == '__main__':
    friends = read_friend_list()
    # analyzes_sex(friends)
    # analyzes_info(friends)
    analyzes_signature(friends)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import session, utils
from bs4 import BeautifulSoup
import bs4
from time import sleep
import random
from threading import Thread
import wordcloud
import jieba
import json
import sys
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
SUBJECT_URL = 'https://movie.douban.com/subject/26322642/'
COMMENTS_INDEX_URL = 'https://movie.douban.com/subject/26322642/comments'
COMMENTS_URL_SCORE = 'https://movie.douban.com/subject/26322642/comments?sort=new_score&status=%s'
COMMENTS_URL_TIME = 'https://movie.douban.com/subject/26322642/comments?sort=time&status=%s'
COMMENTS_URL_FOLLOWS = 'https://movie.douban.com/subject/26322642/follows_comments?status=%s'


session = session()
header = {}
cookie = {}
comment_list = []


def loader_header():
    with open('headers.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            items = line.replace('\n', '').split(':', 1)
            if items[0] == 'Cookie':
                cookie_list = items[1].split(';')
                for cookie_item in cookie_list:
                    cookies = cookie_item.split('=', 1)
                    cookie[cookies[0]] = cookies[1]
            else:
                header[items[0]] = items[1]
    utils.add_dict_to_cookiejar(session.cookies, cookie)
    pass


def checkout_login():
    url = 'https://www.douban.com/accounts/'
    account_page = session.get(url, headers=header, allow_redirects=False)
    print(account_page.status_code)
    with open('account.html', 'wb') as f:
        f.write(account_page.content)
    pass


def get_comments(url=COMMENTS_URL_SCORE):
    comments_page = session.get(url, headers=header, allow_redirects=False)
    html = comments_page.text
    bs = BeautifulSoup(html, 'lxml')

    comment_divs = bs.find_all('div', attrs={'class': 'comment-item'})
    for div in comment_divs:
        comment_p = div.find_all('p', attrs={'class', ''})
        comment = comment_p[0].text.strip().replace('\n', '。') + '\n'
        if comment in comment_list:
            continue
        comment_list.append(comment)

    paginator_divs = bs.findAll(
        'div', attrs={'class': 'center', 'id': 'paginator'})
    if len(paginator_divs) > 0:
        next_page = paginator_divs[0].find_all('a', attrs={'class': 'next'})
        if len(next_page) > 0:
            url_next = '%s%s' % (
                COMMENTS_INDEX_URL, next_page[0]['href'])
            print(url_next)
            sleep(1 + random.randint(0, 5))
            get_comments(url_next)

    pass


def cloud():
    with open('comment.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        cut_text = ''
        for line in lines:
            cut_text += ''.join(jieba.cut(line))
        font_path = 'simfang.ttf'
        mask = np.array(Image.open('sphx_glr_colored_003.png'))
        wc = wordcloud.WordCloud(mask=mask, background_color='white',
                                 max_words=2000, font_path=font_path, width=720, height=1280 )
        wc.generate(cut_text)
        wc.to_file('alice.png')
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.figure()
        plt.show()
    pass


if __name__ == '__main__':
    if sys.argv[1:] and sys.argv[1] == 'wordcloud':
        cloud()
    else:
        loader_header()
        # checkout_login()
        threads = []

        thread1 = Thread(target=get_comments, args=(COMMENTS_URL_TIME % 'p',))
        thread2 = Thread(target=get_comments, args=(COMMENTS_URL_SCORE % 'P',))
        thread3 = Thread(target=get_comments, args=(COMMENTS_URL_TIME % 'F',))
        thread4 = Thread(target=get_comments, args=(COMMENTS_URL_SCORE % 'F',))
        threads.append(thread1)
        threads.append(thread2)
        threads.append(thread3)
        threads.append(thread4)

        for thread in threads:
            thread.start()
            thread.join()

        with open('comment.txt', 'w', encoding='utf-8') as f:
            f.writelines(comment_list)

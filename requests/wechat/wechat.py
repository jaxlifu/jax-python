#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import os
import re
import html2text
import random
from time import sleep
from bs4 import BeautifulSoup
from utils import *

request_headers = '''
Accept:*/*
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.9
Cache-Control:no-cache
Connection:keep-alive
Cookie:wxuin=1475819580; lang=zh_CN; pass_ticket=4RMPwRaTcrK6GwUgnLHVonaGPXr1xF67KUkWub5wOSfSdojVkLHSPY8pJRpaG80S; wxtokenkey=d52d29c8b2ed9c793dc0bdb44ebdd23a593155eeac9dcf2bc82035caa7ab9477; devicetype=Windows10; version=62060038; wap_sid2=CLzw3L8FElxydHUwdkc5WUcxRE9xTWtzNk0yZVRlcE5mMEFxaGMwT1BLUnM3MG01a2tXNGt6bW5JUS1XVGJyNVRiei16YkVnUGFEUmlPUllSWVZGZ3hOZF9wYVBSYVlEQUFBfjD3467RBTgMQJRO
Host:mp.weixin.qq.com
Pragma:no-cache
Referer:https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzA4NTQwNDcyMA==&scene=124&uin=MTQ3NTgxOTU4MA%3D%3D&key=7abe095b989640fce0f77a57d0eb1d90fb7945efe6da1198fafe4f01b898afa25162163bfb8cc560341063fe394197e34107571558455e7fa3cc15402818cfcc8317e4e108976c1ae7efc30be18c6996&devicetype=Windows+10&version=62060038&lang=zh_CN&a8scene=7&pass_ticket=4RMPwRaTcrK6GwUgnLHVonaGPXr1xF67KUkWub5wOSfSdojVkLHSPY8pJRpaG80S&winzoom=1
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36
X-Requested-With:XMLHttpRequest
'''
# 公众号python程序猿
# url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5NzU0MzU0Nw==&f=json&offset={0}&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=&wxtoken=&appmsg_token=934_EbsCZ1RN2YgaW8YZusFtdtsZi_iZ5KDZotQV-g~~&x5=0&f=json'
# 公众号 48号
#url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzI2NzMyNzQ2MA==&f=json&offset={0}&count=10&is_ok=1&scene=124&uin=MTQ3NTgxOTU4MA%3D%3D&key=60adec318085d8259785e9212a82bd3319a5114963900ef0bb116a87a693d40a111ab77eec08f2ce3868621634c985d2f0bbd2f9ce2b05953658a867cac9c9186f9e8fb14ece8b84ab4e8b6fb84634e4&pass_ticket=4RMPwRaTcrK6GwUgnLHVonaGPXr1xF67KUkWub5wOSfSdojVkLHSPY8pJRpaG80S&wxtoken=&appmsg_token=934_ybAUQ3lidIkbi3tyE54BsHf-CjaU38a_REp-2g~~&x5=0&f=json'
# 公众号stormzhang
url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA4NTQwNDcyMA==&f=json&offset={0}&count=10&is_ok=1&scene=124&uin=MTQ3NTgxOTU4MA%3D%3D&key=7abe095b989640fce0f77a57d0eb1d90fb7945efe6da1198fafe4f01b898afa25162163bfb8cc560341063fe394197e34107571558455e7fa3cc15402818cfcc8317e4e108976c1ae7efc30be18c6996&pass_ticket=4RMPwRaTcrK6GwUgnLHVonaGPXr1xF67KUkWub5wOSfSdojVkLHSPY8pJRpaG80S&wxtoken=&appmsg_token=934_Vz7zQEHA81qsEfaxNuwTe0GffNWd-zwbvpnT5g~~&x5=0&f=json'
DIR_NAME = 'download'


class WeChatMp(object):

    def __init__(self):
        self.article_list = []
        self.session = requests.Session()
        self.headers, self.cookies = init_header(request_headers)
        self.url = 'https://mp.weixin.qq.com/mp/profile_ext?'
        requests.utils.add_dict_to_cookiejar(
            self.session.cookies, self.cookies)
        if not os.path.exists(DIR_NAME):
            os.mkdir(DIR_NAME)
        pass

    def _format_url(self, _biz, offset, uin, key, pass_ticket, appmsg_token):

        data = {
            'action': 'getmsg',
            '_biz': _biz,
            'f': 'json',
            'offset': offset,
            'count': '10',
            'is_ok': '1',
            'scene': '124',
            'uin': uin,
            'key': key,
            'pass_ticket': pass_ticket,
            'wxtoken': '',
            'appmsg_token': appmsg_token,
            'x5': '0',
            'f': 'json'
        }
        for key, value in data.item():
            self.url += '%s&%s' % (key, value)
        pass

    def load_history(self, offset=0):
        historyPage = self.session.get(
            url.format(offset), headers=self.headers).json()
        if historyPage['errmsg'] == 'ok' and historyPage['ret'] == 0:
            self._parse_data(historyPage['general_msg_list'])
            if historyPage['can_msg_continue'] == 1:
                next_offset = historyPage['next_offset']
                self.load_history(offset=next_offset)
                sleep(random.randint(0, 5))
        else:
            print(historyPage)
        pass

    def _parse_data(self, data):
        data_list = json.loads(data)
        for item in data_list['list']:
            info = item.get('app_msg_ext_info')
            if not info:
                continue
            title = info['title']
            content_url = info['content_url']
            self._download_article(title, content_url)
            sleep(random.randint(0, 5))
        pass

    def _download_article(self, title, url):
        if not url:
            return
        print(title, url)
        self.article_list.append((title, url))
        # 文件名不能包含以下字符\/:*?"<>|
        # 替换掉以上的特殊字符为_
        title = check_filename(filename=title)
        filename = '{0}/{1}.md'.format(DIR_NAME, title)

        if os.path.exists(filename):
            return
        articlePage = self.session.get(url, headers=self.headers)
        if articlePage.status_code != 200:
            return
        with open(filename, 'w', encoding='utf-8') as f:
            bs = BeautifulSoup(articlePage.text, 'lxml')
            h = html2text.HTML2Text()
            pageContent = bs.find('div', attrs={'id': 'page-content'})
            article = h.handle((str(pageContent)))
            f.write(article)
        pass
    pass


if __name__ == '__main__':
    DIR_NAME = input('请输入文件夹名称: >')
    wechat = WeChatMp()
    wechat.load_history(0)
    with open('articleList.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(wechat.article_list, ensure_ascii=False))

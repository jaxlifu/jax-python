#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests import Request, Session
import json
import re
# 检查用户是否登录
SETTINGS_URL = 'http://www.jianshu.com/settings/basic'
# 用户主页
USER_HOME_URL = 'http://www.jianshu.com/u/%s'


class Jianshu(object):
    def __init__(self):
        self.session = Session()
        self.headers = {}
        self.cookie = {}
        self.user_info = {}
        self.load_headers()
        pass

    def load_headers(self):
        with open('headers.txt', 'r', encoding='utf-8') as f:
            data = f.readlines()
            for line in data:
                line_items = line.replace('\n', '').split(':')
                if line_items[0] == 'Cookie':
                    cookies = line_items[1].split(';')
                    for item in cookies:
                        cookie_item = item.split('=')
                        self.cookie[cookie_item[0]] = cookie_item[1]
                else:
                    self.headers[line_items[0]] = line_items[1]
        pass

    def check_login(self):
        # 禁止重定向来检验用户是否登录
        setting_page = self.session.get(SETTINGS_URL,
                                        headers=self.headers, allow_redirects=False)
        print(setting_page.status_code)
        if setting_page.status_code == 200:
            print('获取用户信息成功')
            self.get_userinfo(setting_page)
            with open('setting.html', 'wb') as f:
                f.write(setting_page.content)
        else:
            requests.utils.add_dict_to_cookiejar(
                self.session.cookies, self.cookie)
            self.check_login()
        pass

    def get_userinfo(self, response):
        if response.status_code == 200:
            html = response.text
            info = re.findall(
                r'<script .*? data-name="page-data">(.*?)</script>', html, re.S)
            self.user_info = json.loads(info[0])
        pass

    def get_user_home(self):
        slug = self.user_info['current_user']['slug']
        user_home_page = self.session.get(USER_HOME_URL % slug)
        with open('homepage.html', 'wb') as f:
            f.write(user_home_page.content)
        pass
    pass


if __name__ == '__main__':
    jianshu = Jianshu()
    jianshu.check_login()
    print(jianshu.user_info)
    jianshu.get_user_home()

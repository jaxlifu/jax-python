#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import os
import MySQLdb
from time import sleep
from bs4 import BeautifulSoup

# 为了防止爬虫被后台发现,导致出现异常,每个请求设置1s间隔
FOLDER_NAME = 'static_file'

URL_PROFILE = 'https://www.zhihu.com/settings/profile'
URL_INDEX = 'https://www.zhihu.com/'
URL_FOLLOWING = 'https://www.zhihu.com/api/v4/members/%s/followees?include=data&offset=0&limit=20'
URL_FOLLOWERS = 'https://www.zhihu.com/api/v4/members/%s/followers?include=data&offset=0&limit=20'


def load_head():
    header = {}
    cookie = {}
    with open('header.txt', 'r', encoding='utf-8') as f:
        data_list = f.readlines()
        for data in data_list:
            item_list = data.replace('\n', '').split(':', 1)
            if item_list[0] == 'Cookie':
                cookie_list = [x.split('=', 1)
                               for x in item_list[1].split(';')]
                for item in cookie_list:
                    cookie[item[0]] = item[1]
            else:
                header[item_list[0]] = item_list[1]
    return header, cookie
    pass


class ZhihuScrapy(object):
    def __init__(self):
        self.header, self.cookie = load_head()
        self.session = requests.Session()
        self.page_number = 1

        self.conn = MySQLConn()
        self.user_link_list = []
        self.user_id_list = []
        self.retry_times = 0
        if not os.path.exists(FOLDER_NAME):
            os.mkdir(FOLDER_NAME)
        os.chdir(FOLDER_NAME)
        pass

    def check_login(self):
        sleep(1)
        if self.retry_times >= 3:
            print('3次登录重试失败')
            return
        self.retry_times = self.retry_times + 1
        profile_page = self.session.get(
            URL_PROFILE, headers=self.header, allow_redirects=False)
        if profile_page.status_code == 200:
            print('获取用户信息成功')
            return True
        else:
            requests.utils.add_dict_to_cookiejar(
                self.session.cookies, self.cookie)
            self.check_login()
            return False
        pass

    def get_data_info(self, html_text=None):
        bs = BeautifulSoup(html_text, 'lxml')
        data_info = bs.find_all(
            'div', {'id': 'data', 'style': 'display:none;'})
        if not data_info:
            return
        # 直接获取到的数据时经过了转义的,用json解析再存储
        data_json = json.loads(data_info[0]['data-state'], encoding='utf-8')
        return data_json
        pass

    def get_home_page(self):
        sleep(1)
        user_list = []
        home_page = self.session.get(URL_INDEX, headers=self.header)
        if home_page.status_code != 200:
            print('get home page fail %s' % home_page.status_code)
            return
        data_json = self.get_data_info(home_page.text)
        if not data_json:
            return
        answers = data_json['entities']['answers']
        for key, value in answers.items():
            author = value['author']
            if author['url'] and not author['id'] in self.user_id_list:
                self.user_id_list.append(author['id'])
                self.user_link_list.append(author)
                self.get_user_home(url=author['url'])
                self.get_user_follow(
                    url=URL_FOLLOWERS % author['urlToken'])
                self.get_user_follow(
                    url=URL_FOLLOWING % author['urlToken'])
        self.get_next_page(url=data_json['topstory']['topstorys']['next'])
        pass

    def get_user_follow(self, url):
        sleep(1)
        followers_page = self.session.get(url, headers=self.header)
        if followers_page.status_code != 200:
            print('get follow page fail %s' % followers_page.status_code)
            return
        data = json.loads(followers_page.text, encoding='utf-8')
        if data.get('data'):
            for user in data['data']:
                if user['url'] and not user['id'] in self.user_id_list:
                    self.get_user_home(url=user['url'])
                    self.user_link_list.append(user)
                    self.user_id_list.append(user['id'])
        # 加载下一页
        if data['paging'] and not data['paging']['is_end']:
            self.get_user_follow(data['paging']['next'])
        pass

    def get_user_home(self, url=''):
        return
        user_home_page = self.session.get(url, headers=self.header)
        if user_home_page.status_code != 200:
            print('get user home page fail %s' % user_home_page.status_code)
            return
        data = json.loads(user_home_page.text, encoding='utf-8')
        user_id = data.get('id')  # 用户id
        name = data.get('name')  # 用户名
        gender = data.get('gender')  # 0--女 1--男 -1--未知
        url_token = data.get('url_token')  # 用户token
        headline = data.get('headline')  # 用户自我介绍
        description = data.get('description')  # 用户描述
        avatar_url = data.get('avatar_url')  # 头像
        business = data.get('business')  # 行业信息
        location = data.get('location')  # 位置信息
        education = data.get('education')  # 教育经历
        employments = data.get('employments')  # 职业经历
        following_count = data.get('following_count')  # 关注了
        follower_count = data.get('follower_count')  # 关注者
        answer_count = data.get('answer_count')  # 回答
        question_count = data.get('question_count')  # 提问
        articles_count = data.get('articles_count')  # 文章
        columns_count = data.get('columns_count')  # 专栏
        pins_count = data.get('pins_count')  # 想法
        is_bind_sina = data.get('is_bind_sina')  # 是否绑定新浪微博
        pass

    def get_next_page(self, url=''):
        sleep(1)
        headers = self.header
        headers['X-API-VERSION'] = '3.0.53'
        headers['X-UDID'] = 'ABCCrHc7sQyPTiwbIdNYkR9r7fp40fVB6mg='
        headers['authorization'] = 'Bearer Mi4xcERiZUFRQUFBQUFBRUlLc2R6dXhEQmNBQUFCaEFsVk53TWI2V2dCTTU2RXp6QjBHVmtlalFtNHlrUUhtZTJYYzl3|1510832320|dd54d65b14f7c667f8d7ec54c9b61a8f46285f0c'
        topstory_page = self.session.get(url, headers=headers)
        if topstory_page.status_code != 200:
            print('get get_next_page fail %s' % topstory_page.status_code)
            return
        print('开始分析第%d页数据' % self.page_number, 'url == %s' % url)
        is_end, next_page, previous_page = self.parse_data(topstory_page.text)
        # 获取下一页
        if not is_end:
            self.get_next_page(url=next_page)
        pass

    def parse_data(self, data=None):
        if not data:
            return

        data_json = json.loads(data, encoding='utf-8')
        is_end = data_json['paging']['is_end']
        next_page = data_json['paging']['next']
        previous_page = data_json['paging']['previous']
        datas = data_json['data']
        try:
            for item in datas:
                author = item['target']['author']
                if author['url'] and not author['id'] in self.user_id_list:
                    self.get_user_home(url=author['url'])
                    self.user_link_list.append(author)
                    self.user_id_list.append(author['id'])
        except Exception as e:
            print(e)
        return is_end, next_page, previous_page
        pass
    pass


class MySQLConn(object):

    def __init__(self):
        self.conn = MySQLdb.connect(
            host='127.0.0.1', user='root', passwd='',
            port=3306, db='zhihu_user', charset='utf8'
        )
        pass

    def cursor(self):
        return self.conn.cursor()
        pass

    def close(self):
        self.conn.cursor().close()
        self.conn.close()
        pass

    def drop_table(self):
        sql = 'DROP TABLE IF EXISTS `user_link`'
        self.cursor().execute(sql)
        pass

    def create_table(self):
        sql = '''CREATE TABLE `user_link` (
            	id INT auto_increment PRIMARY KEY,
            	user_name VARCHAR (50),
            	user_link VARCHAR(200),
            	user_id VARCHAR(50))
        '''
        self.cursor().execute(sql)
        pass

    def update(self):
        pass

    def insert(self, data=None):
        if not data:
            return
        sql = '''INSERT INTO user_link (user_name,user_link,user_id)VALUES(%s,%s,%s)'''
        param = [(author['name'], author['url'], author['id'])
                 for author in data]
        self.cursor().executemany(sql, param)
        self.conn.commit()
        pass

    def delete(self):
        pass

    def query(self):
        pass
    pass


if __name__ == '__main__':
    zhihu = ZhihuScrapy()
    zhihu.conn.drop_table()
    zhihu.conn.create_table()
    try:
        zhihu.check_login()
        zhihu.get_home_page()
    except Exception as e:
        print('requests error %s' % e)
    zhihu.conn.query()
    zhihu.conn.insert(data=zhihu.user_link_list)
    zhihu.conn.close()

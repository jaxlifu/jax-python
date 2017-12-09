#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
import time
import os
try:
    import cookielib
except:
    import http.cookiejar as cookielib
from PIL import Image


def log(*messages):
    for message in messages:
        print('=================\n%s\n=================' % message)
    pass


URL_INDEX = 'https://www.zhihu.com'
URL_PROFILE = 'https://www.zhihu.com/settings/profile'
URL_LOGIN_EMAIL = 'https://www.zhihu.com/login/email'
URL_LOGIN_PHONE = 'https://www.zhihu.com/login/phone_num'
URL_CAPTCHA = 'https://www.zhihu.com/captcha.gif?r=%s&type=login'

# 使用登录的session信息
session = requests.Session()
session.cookies = cookielib.LWPCookieJar(filename='cookies')
try:
    session.cookies.load(ignore_discard=True)
except Exception as e:
    log('cookie load file %s' % e)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.zhihu.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
}


# 校验是否登录
def check_login():
    r = session.get(URL_PROFILE, headers=headers, allow_redirects=False)
    log(r.status_code)
    return True if r.status_code == 200 else False
    pass


def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_page = session.get(URL_CAPTCHA % t, headers=headers)
    with open('captcha.png', 'wb') as f:
        f.write(captcha_page.content)
        f.close()
    try:
        img = Image.open('captcha.png', mode="r")
        img.show()
        img.close()
    except:
        print('请找到%s下的captcha.png输入验证码' % os.path.abspath('captcha.png'))
    captcha = input('请输入验证码:\n')
    return captcha
    pass


def get_xsrf():
    index_page = session.get(URL_INDEX, headers=headers)
    html = index_page.text
    pattern = r'name="_xsrf" value="(.*?)"'
    _xsrf = re.findall(pattern, html)
    return _xsrf[0] if len(_xsrf) > 0 else ''
    pass


def post_login(url, data, headers):
    login_page = session.post(url, data=data, headers=headers)
    result = login_page.json()
    print(result)
    return result
    pass


def login(username, password):
    url = ''
    account = ''
    _xsrf = get_xsrf()
    if re.match(r'^1\d{10}$', username):
        print('手机号登录')
        url = URL_LOGIN_PHONE
        account = 'phone_num'
    elif '@' in username:
        print('邮箱登录')
        url = URL_LOGIN_EMAIL
        account = 'email'
    else:
        print('账号输入错误')
        return

    if len(password) < 6 and len(password) > 20:
        print('请输入6-20位的密码')
        return

    postdata = {
        '_xsrf': _xsrf,
        'password': password,
        account: username
    }

    # 先不用密码直接登录
    if post_login(url, postdata, headers)['r'] == 1:
        print('获取验证码重新登录')
        postdata['captcha'] = get_captcha()
        post_login(url, postdata, headers)
    session.cookies.save()
    pass


if __name__ == '__main__':
    if check_login():
        log('你已经登录')
    else:
        log('请输入用户名和密码登录')
        username = input('请输入用户名:\n')
        password = input('请输入密码:\n')
        login(username, password)

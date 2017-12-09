#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from requests import Session
import re
import random
import json
base_requests_headers = '''
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.8
Cache-Control:no-cache
Cookie:BAIDUID=AC4103895E462F08DC7341CD4C2681E6:FG=1; BIDUPSID=AC4103895E462F08DC7341CD4C2681E6; PSTM=1510385220; BDUSS=VxaVd5ZjBkWWpGcnc1R3ZTM25oZm5vQzdtdkxMYkc0U2pLODMtSUw5Unc2MFphSVFBQUFBJCQAAAAAAAAAAAEAAAATpzcvc21pbGXXz9y~wlEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBeH1pwXh9aVl; userid=792176403; token_=6918210a424C4744424341454615120052337173fc3624861a62bd798483cfa3; pgv_pvi=647161856; sttbHint=sttbHintShow; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=6; H_PS_PSSID=1458_21090_25178; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; Hm_lvt_b0e17e90eff522755fac9e19f71a97f7=1512526295,1512527788; Hm_lpvt_b0e17e90eff522755fac9e19f71a97f7=1512527788; tip_show_limit=5; BDRCVFR[_ZrbkGSZBxf]=mk3SLVN4HKm; firstShowTip=1; shituhistory=%7B%220%22%3A%22http%3A%2F%2Ff.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2Fa6efce1b9d16fdfad2bcf46ebf8f8c5495ee7b59.jpg%22%2C%221%22%3A%22http%3A%2F%2Fc.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2Fa71ea8d3fd1f4134355237fe2e1f95cad0c85ecc.jpg%22%2C%222%22%3A%22http%3A%2F%2Ff.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2F279759ee3d6d55fb97e846a666224f4a20a4dd07.jpg%22%2C%223%22%3A%22http%3A%2F%2Fc.hiphotos.baidu.com%2Fimage%2Fpic%2Fitem%2F94cad1c8a786c917cdd199a6c23d70cf3ac7575b.jpg%22%7D; Hm_lvt_9a586c8b1ad06e7e39bc0e9338305573=1512526305; Hm_lpvt_9a586c8b1ad06e7e39bc0e9338305573=1512528462; indexPageSugList=%5B%22http%3A%2F%2Femoji.qpic.cn%2Fwx_emoji%2FuFHlM7Wh33IGlfYjRsp5jiadjrjX2bBSY32dFcUEgRCPGGE8bXaGlg7UqGxDjl74ib%2F%22%5D; cleanHistoryStatus=0; userFrom=null; uploadTime=1512528573004
Host:image.baidu.com
Pragma:no-cache
Proxy-Connection:keep-alive
Referer:http://image.baidu.com/
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36
'''

image_requests_headers = '''
Accept:image/webp,image/apng,image/*,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.8
Cache-Control:no-cache
Host:img1.imgtn.bdimg.com
Pragma:no-cache
Proxy-Connection:keep-alive
Referer:http://image.baidu.com/pcdutu?queryImageUrl=http://img3.imgtn.bdimg.com/it/u=3585125182,1151099867&fm=27&gp=0.jpg&fm=index&uptype=paste&vs=9fd005d7bab471a63c2302fb21c275a1dbfc5271
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36
'''
session = Session()
headers = {}
image_headers = {}
cookies = {}
test_url = 'http://emoji.qpic.cn/wx_emoji/uFHlM7Wh33IGlfYjRsp5jiadjrjX2bBSY32dFcUEgRCPGGE8bXaGlg7UqGxDjl74ib/'


def _base_headers():
    lines = base_requests_headers.split('\n')
    lines = [item for item in lines if item.strip()]
    for line in lines:
        items = line.split(':', 1)
        if items[0] == 'Cookie':
            for cookie_line in items[1].split(';', 1):
                cookie_items = cookie_line.split('=', 1)
                cookies[cookie_items[0]] = cookie_items[1]
        else:
            headers[items[0]] = items[1]
    requests.utils.add_dict_to_cookiejar(session.cookies, cookies)
    pass


def _image_headers():
    lines = image_requests_headers.split('\n')
    lines = [item for item in lines if item.strip()]
    for line in lines:
        items = line.split(':', 1)
        image_headers[items[0]] = items[1]
    pass


def init_headers():
    _base_headers()
    _image_headers()
    pass


def baidu_image(queryImageUrl=None):
    if not queryImageUrl:
        return
    url = 'http://image.baidu.com/pcdutu?'
    similist = None
    data = {
        'queryImageUrl': queryImageUrl,
        'fm': 'index',
        'uptype': 'paste',
        'vs': '3deef828447f5ff536c613485d05ceafa7015901'
    }
    for key, value in data.items():
        url += '%s=%s&' % (key, value)
    result = session.get(url, headers=headers)

    data_result = re.findall(r'<script>(.*?)</script>', result.text, re.S)
    data_result = [item.strip()
                   for item in data_result if 'window.bd' in item]
    data_result = data_result[0] if data_result and len(
        data_result) > 0 else ''
    for line in data_result.strip().split('\n'):
        if 'simiList' in line:
            similist = json.loads(line[0:-1].replace('simiList: ', ''))
            break
    if similist:
        simiItem = similist[random.randint(0, len(similist))]
        return simiItem['ThumbnailURL']
    pass


def search_emoji(keywork):
    url = 'http://www.doutula.com/search?keyword=%s' % keywork
    page = session.get(url, headers=headers)
    bs = BeautifulSoup(page.text, 'lxml')
    divs = bs.find_all(name='div', attrs={'class': 'random_picture'})
    imgs = divs[0].find_all(
        name='img', attrs={'class': 'img-responsive lazy image_dtb'})
    pictures = [picture['data-original'] for picture in imgs]
    picture_url = pictures[random.randint(0, len(pictures - 1))]
    download_picture(picture_url)
    pass


def load_baidu_image(cdnurl):
    filename = None
    returnUrl = baidu_image(cdnurl)
    filename = download_picture(returnUrl)
    return filename
    pass


def download_picture(url):
    picture = session.get(url, headers=image_headers)
    if picture.status_code != 200:
        return False
    filename = 'download/%s' % [
        name for name in url.split('/') if name != ''][-1]
    with open(filename, 'wb') as f:
        f.write(picture.content)
        f.close()
    return filename
    pass

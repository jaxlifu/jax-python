#!/usr/bin/env python
# -*- coding=utf-8 -*-
import base64
import os
import re

import requests
from bs4 import BeautifulSoup

from utils import *

DOWNLOAD_DIR ='download'


request_header = '''
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Cache-Control:no-cache
Cookie:__cfduid=d5ef94fc0f64f439db22401cec4e6ffb71513415905; UM_distinctid=1605e9e0edc1fb-034870bed6ef28-b7a103e-15f900-1605e9e0edd7bb; ASPSESSIONIDASTRDABS=KJCMEGGCNELCOFINKIMKCLGP; yjs_id=TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzYzLjAuMzIzOS44NCBTYWZhcmkvNTM3LjM2fHd3dy41MTdtaC5uZXR8MTUxMzQxNTkwNTM0M3xodHRwczovL3d3dy5nb29nbGUuY29tLmhrLw; ctrl_time=1; bdshare_firstime=1513415906685; Pmy=; CNZZDATA1263795027=1693548171-1513410836-https%253A%252F%252Fwww.google.com.hk%252F%7C1513416236; qtmhhis=2017-11-16-17-25-12%5E%5E%u6211%u7684%u53CC%u4FEE%u9053%u4FA3%uFF08%u6211%u7684%u5929%u52AB%u5973%u53CB%uFF09%5E%5E%u7B2C152%u8BDD%20%u5E08%u59D0%u7684%u5B9E%u529B%5E%5E1%5E%5E159528%5E%5E9655_ShG_
Host:www.517mh.net
Pragma:no-cache
Proxy-Connection:keep-alive
Referer:http://www.517mh.net/comic/9655/159528.html
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36
'''
HOST_URL = 'http://www.517mh.net'
BASE_URL = 'http://www.517mh.net/comic/9655/'

class Comic(object):
    def __init__(self, *args, **kwargs):
        self.headers,self.cookie = init_header(request_header)
        self.session = requests.Session()
        requests.utils.add_dict_to_cookiejar(self.session.cookies,self.cookie)
        pass

    def load_comic_directory(self):
        dir_page = self.session.get(BASE_URL, headers=self.headers)
        if dir_page.status_code!=200:
            return
        dir_page.encoding = 'GBK'
        bs = BeautifulSoup(dir_page.text,'lxml')
        chapter_divs = bs.find_all('div', attrs={'class': 'chapter-list cf mt10'})
        for item in chapter_divs:
            links = item.find_all('a', attrs={'class': 'status0'})
            for link in links:
                print(link.get('title'), HOST_URL + link.get('href'))
                self.load_comic_content(HOST_URL + link.get('href'))
                break
        pass

    def load_comic_content(self,url,title):
        content_page = self.session.get(url,headers=self.headers)
        if content_page.status_code!=200:
            return

        content_page.encoding ='GBK'
        urls = re.findall(r'var qTcms_S_m_murl_e="(.*?)";',content_page.text,re.S)
        for url in urls:
            url = base64.b64decode(url)
            img_urls = str(url).split('$qingtiandy$')
            for img_url in img_urls:
                self.download_image(img_url, '%s/%s' % (DOWNLOAD_DIR, title))
        pass

    def download_image(self,url,path):
        image_page=self.session.get(url,headers=self.headers)
        if image_page.status_code!=200:
            pass
        filename = '%s/%s' % (path,url.split('/')[-1])
        if os.path.exists(filename,'wb') as f:
            f.write(image_page.content)
        pass

    pass
def main():
    if not os.path.exists(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    comic= Comic()
    comic.load_comic_directory()
    pass

if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests

SUPPORT_LIST = ['zh-CHS', 'ja', 'EN', 'ko', 'fr', 'ru', 'pt', 'es']

class Translation(object):

    def __init__(self):
        self.session = requests.Session()
        self.header, self.cookie = self.load_headers()
        requests.utils.add_dict_to_cookiejar(self.session.cookies, self.cookie)
        pass

    def load_headers(self):
        header = {}
        cookie = {}
        with open('headers.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                items = line.replace('\n', '').split(':', 1)
                if items[0] == 'Cookie':
                    cookies = [x.split('=', 1) for x in items[1].split(';', 1)]
                    for cookie_item in cookies:
                        cookie[cookie_item[0]] = cookie_item[1]
                else:
                    header[items[0]] = items[1]
        return header, cookie
        pass

    def translation_keyword(self, keyword):
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        data = {}
        data['i'] = keyword
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = '1512198205569'
        data['sing'] = '8bc3ca1d44b61fdd5e244b9213ab05d8'
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_REALTIME'
        data['typoResult'] = 'true'
        page = self.session.post(url, data=data, headers=self.header)
        result = eval(page.text)
        print(result,result.get('translateResult')[0][0]['tgt'])
        pass
    pass


if __name__ == '__main__':
    t = Translation()
    keyword = input('请输入要翻译的内容\n>')
    print(keyword)
    t.translation_keyword(keyword)

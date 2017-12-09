#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import xml.etree.cElementTree as ET
import random
import json
import hashlib

XLIFF = 'urn:oasis:names:tc:xliff:document:1.2'
APP_ID = '4753a0c015527986'
SECRET_KEY = 'IzMI42dDoINedpFI46002lZoOq8kyuzE'
SUPPORT_LIST = ['zh-CHS', 'ja', 'EN', 'ko', 'fr', 'ru', 'pt', 'es']
URL = 'http://openapi.youdao.com/api?'


class Translation(object):
    def __init__(self, _from='auto', _to='zh-CHS'):
        # xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2"
        ET.register_namespace('xliff', XLIFF)
        self.session = requests.Session()
        self._from = _from
        self._to = _to
        pass

    def load_xml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        root.getchildren()
        self.format_xml(root)
        tree.write('strings_%s.xml' % self._to, encoding='utf-8')
        pass

    def format_xml(self, element):
        if element.tail and element.tail.strip():
            result = self.translation_keyword(element.tail)
            if result and len(result) > 0:
                element.tail = result[0]

        if XLIFF not in element.tag and element.text and element.text.strip():
            result = self.translation_keyword(element.text)
            if result and len(result) > 0:
                element.text = result[0]
        else:
            for child in element:
                self.format_xml(child)
        pass

    def translation_keyword(self, keyword):
        url = self.format_url(keyword)
        page = self.session.get(url)
        result = json.loads(page.text)
        print(keyword, result.get('translation'))
        return result.get('translation')
        pass

    def format_url(self, q):
        params = {}
        salt = str(random.randint(1, 65535))
        sign = APP_ID + q + salt + SECRET_KEY
        sign = hashlib.md5(sign.encode(encoding='utf_8')).hexdigest()
        params['q'] = q
        params['from'] = self._from
        params['to'] = self._to
        params['appKey'] = APP_ID
        params['salt'] = salt
        params['sign'] = sign
        url = URL
        for key, value in params.items():
            url += '%s=%s&' % (key, value)
        return url
        pass

    pass

#会识别到当前同级目录下的strings.xml文件
#然后对文件进行翻译,用的是有道翻译api所以只支持
if __name__ == '__main__':
    language_from = 'auto'
    length_list = []
    for i in range(0, len(SUPPORT_LIST)):
        length_list.append(i)
    support_dict = dict(zip(length_list, SUPPORT_LIST))
    index = input('请输入下列序号选择源语言\n%s\n>' % support_dict)
    try:
        language_from = support_dict[int(index)]
    except:
        print('输入格式有误,自动识别目标语言')

    for language in SUPPORT_LIST:
        if language == language_from:
            continue
        translation = Translation(_from=language_from, _to=language)
        translation.load_xml(filename='strings.xml')

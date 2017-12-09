# -*- coding: utf-8 -*-
import scrapy


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        print('=======\n %s \n========' % response.body)
        with open('baidu.html', 'wb') as file:
            file.write(response.body)
            file.close()
        pass

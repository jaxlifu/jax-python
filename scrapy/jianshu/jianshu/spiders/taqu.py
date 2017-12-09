# -*- coding: utf-8 -*-
import scrapy


class TaquSpider(scrapy.Spider):
    name = 'taqu'
    allowed_domains = ['http://app.taqu.cn/']
    start_urls = ['http://app.taqu.cn/']

    def parse(self, response):
        with open('taqu.html','wb') as file:
            file.write(response.body)
            file.close()

        pass

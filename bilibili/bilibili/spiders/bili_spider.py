# -*- coding: utf-8 -*-
import scrapy
import os


class BiliSpiderSpider(scrapy.Spider):
    name = "bili_spider"
    allowed_domains = ["http://www.bilibili.com"]
    start_urls = ['http://www.bilibili.com/']

    def parse(self, response):
        #print("scrapy get bilibili result is ===> \n %s" % response.body)
        # fd = open("bilibili.log", 'wb')
        # fd.write(response.body)
        # fd.close()
        item = BilibiliItem()
        for sel in response.xpath('//ul/li'):
            item.name = sel.xpath('a/text()').extract()
            item.link = sel.xpath('a/@href').extract()
            item.desc = sel.xpath('text()').extract()
        yield item

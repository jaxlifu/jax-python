# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    nickname = scrapy.Field()
    avatar = scrapy.Field()
    time = scrapy.Field()
    message = scrapy.Field()
    read = scrapy.Field()
    comment = scrapy.Field()
    like = scrapy.Field()
    money = scrapy.Field()
    pass

class zhihuItem(scrapy.Item):
    qestionTitle = scrapy.Field()
    image_urls = scrapy.Field()
    pass

# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import JianshuItem

ROOT_HOST = 'http://www.jianshu.com'
IMAGE_HOST = 'http:'


class HomeSpider(scrapy.Spider):
    name = 'home'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['https://www.jianshu.com/']
    headers = {
        "Host": "www.jianshu.com",
        "Proxy-Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "If-None-Match": 'W/"e87f916af0dc7c37f96a1f73e200c0f2"',
    }

    def parse(self, response):

        with open('jianshu.html', 'wb') as f:
            f.write(response.body)
            f.close()

        selector = scrapy.Selector(response)
        item = JianshuItem()
        notes = selector.xpath('//li[contains(@id,"note-")]')
        for note_item in notes:
            links = note_item.xpath('a[@class="wrap-img"]/@href').extract()
            images = note_item.xpath('a[@class="wrap-img"]/img/@src').extract()
            content = note_item.xpath('div[@class="content"]')
            meta = content.xpath('div[@class="meta"]')

            avatars = content.xpath(
                'div[@class="author"]/a[@class="avatar"]/img/@src').extract()
            nicknames = content.xpath(
                'div[@class="author"]/div[@class="info"]/a/text()').extract()
            times = content.xpath(
                'div[@class="author"]/div[@class="info"]/span[@class="time"]/@data-shared-at').extract()
            collection_tags = meta.xpath(
                'a[@class="collection-tag"]/text()').extract()
            reads = meta.xpath('a[2]/text()').extract()
            comments = meta.xpath(
                'a[3]/text()').extract()
            likes = meta.xpath(
                'span[1]/text()').extract()
            moneys = meta.xpath(
                'span[2]/text()').extract()
            titles = content.xpath('a[@class="title"]/text()').extract()
            messages = content.xpath('p[@class="abstract"]/text()').extract()
            # 部分没有图片的
            item['link'] = ROOT_HOST + links[0] if len(links) > 0 else ''
            item['image'] = IMAGE_HOST + images[0] if len(images) > 0 else ''
            item['avatar'] = IMAGE_HOST + \
                avatars[0] if len(avatars) > 0 else ''
            item['nickname'] = nicknames[0] if len(nicknames) > 0 else ''
            item['time'] = times[0] if len(times) > 0 else ''
            item['title'] = titles[0] if len(titles) > 0 else ''
            item['message'] = messages[0] if len(messages) > 0 else ''
            item['read'] = reads[1].strip() if len(reads) > 1 else '0'
            item['comment'] = comments[1].strip() if len(comments) > 1 else '0'
            item['like'] = likes[0].strip() if len(likes) > 0 else '0'
            item['money'] = moneys[0].strip() if len(moneys) > 0 else '0'

            yield item
        pass

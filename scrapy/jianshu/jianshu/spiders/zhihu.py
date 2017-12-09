# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 用来验证是否登录
    url_profile = 'https://www.zhihu.com/settings/profile'

    def start_requests(self):
        self.log('===============start_requests,get user info settings profile')
        yield Request(self.url_profile,callback=self.check_login)

    # 检验是否登录
    def check_login(self, response):
        self.log('==============check_login')
        pass

    # 没有登录则获取验证码登录
    def get_captcha(self, response):
        pass

    def parse(self, response):
        pass

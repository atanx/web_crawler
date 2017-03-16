# -*- coding: utf-8 -*-
import scrapy
import re

class BaiduSpider(scrapy.Spider):
    name = "Baidu"
    allowed_domains = ["baidu.com"]

    def __init__(self, wd=u'别墅', *args, **kwargs):
        super(BaiduSpider, self).__init__(self, **kwargs)
        self.wd = re.split(',|;', wd)

    def start_requests(self):
        for wd in self.wd:
            url = "https://www.baidu.com/s?wd=%s" % wd
            yield scrapy.Request(url=url, callback=self.parse, meta={'wd': wd})

    def parse(self, response):
        title = response.xpath()
        content = response.xpath()
        url = response.xpath()
        is_ads = response.xpath()
        pass

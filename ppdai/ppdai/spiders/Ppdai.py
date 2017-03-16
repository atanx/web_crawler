# -*- coding: utf-8 -*-
import scrapy


class PpdaiSpider(scrapy.Spider):
    name = "Ppdai"
    allowed_domains = ["ppdai.com"]
    start_urls = (
        'http://www.ppdai.com/',
    )

    def parse(self, response):
        load_id = response.meta['load_id']
        user_profile =response.xpath('//a[@class="username"]/@href').extract_first() or ""
        name = response.xpath('//a[@class="username"]/text()').extract_first() or ""
        title = response.xpath('//h3/span/text()').extract_first() or ''
        rate =
        term =
        mode =
        lend_num =
        end_time =
        status =
        lends =
        gender =
        age =
        education =
        school =
        study =

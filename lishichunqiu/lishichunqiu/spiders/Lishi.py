# -*- coding: utf-8 -*-
import scrapy
import re


class LishiSpider(scrapy.Spider):
    name = "Lishi"
    allowed_domains = ["lishichunqiu.com"]
    start_urls = (
        'http://www.lishichunqiu.com/shanggu/',
    )

    def start_requests(self):
        menus = [('http://www.lishichunqiu.com/shanggu/', '上古')
                 ]
        for m in menus:
            url = m[0]
            dynasty = m[1]
            meta = {'dynasty': dynasty}
            yield scrapy.Request(url, callback=self.parse_list, meta=meta)

    def parse(self, response):
        """
        解析二级目录
        :param response:
        :return:
        """
        menus = response.xpath('//div[@id="main-menu-menu"]//a')
        for menu in menus:
            url = menu.xpath('./@href').extract_first()
            category = menu.xpath('./text()').extract_first()
            meta = {'category': category,
                    'dynasty': response.meta.get('dynasty')
                    }
            yield scrapy.Request(url, callback=self.parse_list, meta=meta)

    def parse_list(self, response):
        meta = {'dynasty': response.meta.get('dynasty'),
                'category': response.meta.get('category')
                }
        next_page = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        article_urls = response.xpath('//td[@class="news_list"]//table[@class="box"]//li/a/@href')
        for article_url in article_urls:
            yield scrapy.Request(article_url, callback=self.parse_article, meta=meta)
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_list, meta=meta)

    def parse_article(self, response):
        dynasty = response.meta.get('dynasty')
        category = response.meta.get('category')
        content = response.meta.get('content', '')
        title = response.xpath('//h1/text()').extract_first()
        info_text = response.xpath('//td[@class="info_text"]/text()').extract_first() or ""
        info_text = info_text.strip('&nbsp;')
        # date
        results = re.findall(u"时间：(\d{4}-\d{2}-\d{2}).*来源：(\S+).*作者：(\S+)", info_text)
        date = _from = author = ''
        if results:
            date, _from, author = results[0]
        # content
        content += "".join(response.xpath('//td[@id="text"]//p[not(@*)]/text()').extract())
        meta = {
            'dynasty': dynasty,
            'category': category,
            'content': content
        }
        # tags
        tag_list = response.xpath('//a[contains(@href,"tags")]/text()').extract()
        tags = ','.join(tag_list)
        next_page = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_article, meta=meta)
        else:
            item = {
                'dynasty': dynasty,
                'category': category,
                'date': date,
                'from': _from,
                'author': author,
                'content': content,
                'tags': tags
            }
            yield item

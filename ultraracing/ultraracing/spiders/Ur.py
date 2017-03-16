# -*- coding: utf-8 -*-
import scrapy
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UrSpider(scrapy.Spider):
    name = "Ur"
    allowed_domains = ["ultraracing.my"]
    start_urls = (
        'http://ultraracing.my/ecatalog/',
    )

    def parse(self, response):
        urls = response.xpath('//ul[@class="product-categories"]//ul[@class="children"]//li/a/@href').extract()
        for url in urls:
            meta = dict(url=url)
            yield scrapy.Request(url, callback=self.parse_list, meta=meta)

    def parse_list(self, response):
        url = response.meta['url']
        parts = url.split('/')
        model = parts[-2]
        brand = parts[-3]
        meta = {'url': response.url,
                'brand': brand,
                'model': model}
        urls = response.xpath(u'//div[@class="product-wrap"]//div[@class="cg-product-info"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item, meta=meta)

    def parse_item(self, response):
        # brand, model, item_title, code, specification, desc, link
        brand = model = title = code = specification = description = link = ''
        brand = response.meta['brand']
        model = response.meta['model']
        title = (response.xpath(u'//h1/text()').extract_first() or '').strip()
        description = response.xpath(u'//div[@class="row"]//div[@itemprop="description"][1]/p/text()').extract()
        description = [i.strip() for i in description]
        description = '\t'.join(description).replace(u'\xa0', ' ')
        code_list = re.findall(u'Code: (\S+-\S+-\S+)', description)
        if code_list:
            code = code_list[0]
        specification_list = re.findall(u'Specification: (.*?)\t', description)
        if specification_list:
            specification = specification_list[0]
        link = response.url
        print u'{brand},{model},{title},{code},{specification},{description},{link}'.format(
            brand=brand,
            model=model,
            title=title,
            code=code,
            specification=specification,
            description=description,
            link=link)
        item = dict(brand=brand,
                    model=model,
                    title=title,
                    code=code,
                    specification=specification,
                    description=description,
                    link=link)
        yield item

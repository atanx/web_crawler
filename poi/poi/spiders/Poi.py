# -*- coding: utf-8 -*-
import scrapy


class PoiSpider(scrapy.Spider):
    name = "Poi"
    allowed_domains = ["poi86.com"]

    def __init__(self, category='47'):
        super(PoiSpider, self).__init__()
        self.category = category

    def start_requests(self):
        yield scrapy.Request('http://www.poi86.com/poi/category/%s/1.html' % self.category)

    def parse(self, response):
        trs = response.xpath('//div[@class="layout"]//tr')
        for tr in trs[1:]:
            url = tr.xpath('./td[1]/@href').extract_first() or ''
            url = response.urljoin(url)
            name = tr.xpath('./td[1]//text()').extract_first() or ''
            address = tr.xpath('./td[2]/text()').extract_first() or ''
            phone = tr.xpath('./td[3]/text()').extract_first() or ''
            district = tr.xpath('./td[4]//text()').extract_first() or ''
            district_url = tr.xpath('./td[4]/a/@href').extract_first() or ''
            district_url = response.urljoin(district_url)
            item = dict(url=url.strip(),
                        name=name.strip(),
                        address=address.strip(),
                        phone=phone.strip(),
                        district=district.strip(),
                        district_url=district_url.strip())
            yield item
        next_page = response.xpath(u'//a[text()="下一页"]/@href').extract_first()
        if len(trs) == 0:
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


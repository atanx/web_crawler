# -*- coding: utf-8 -*-
import scrapy
import re
from os.path import dirname, join
import requests


class MobilebaiduSpider(scrapy.Spider):
    name = "MobileBaidu"
    allowed_domains = ["baidu.com"]
    custom_settings = {'USER-AGENT':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36'}

    def __init__(self, csv='', page_limit=1, **kwargs):
        super(MobilebaiduSpider, self).__init__(self, **kwargs)
        self.page_limit = int(page_limit)
        self.csv = csv

    def start_requests(self):
        f = open(self.csv)
        for word in f.readlines():
            word = word.decode('gbk').strip()
            if not word:
                continue
            url = u"https://m.baidu.com/s?wd=" + word
            request = scrapy.Request(url=url, callback=self.parse)
            request.meta['word'] = word
            request.meta['result_id'] = 0
            request.meta['page_id'] = 1
            yield request

    def parse(self, response):
        results = response.xpath('//div[contains(@class,"c-container ec_resitem") or @class="c-container"]')
        word = response.meta.get('word', '')
        result_id = response.meta.get('result_id', 0)
        page_id = response.meta.get('page_id', 1)
        page_id += 1
        for result in results:
            is_ad = u''
            ad = result.xpath(u'.//span[text()="广告"]')
            if ad:
                is_ad = u'推广'
            title = "".join(result.xpath(u'.//h3//text()').extract())
            url = result.xpath(u'.//a[contains(@class, "c-blocka")]/@href').extract_first() or u''
            abstract = "".join(result.xpath(u'.//*[contains(@class, "c-line-clamp")]//text()').extract())
            #show_url = self.get_real_url(url)
            result_id += 1
            item = {'keyword': word,
                   'title': title,
                   'abstract': abstract,
                   'url': url,
                   'show_url': url,
                   'is_ad': is_ad}
            if url:
                request = scrapy.Request(url, callback=self.parse_real_url)
                request.meta['word'] = word
                request.meta['result_id'] = result_id
                request.meta['page_id'] = page_id
                request.meta['item'] = item
                request.meta['dont_redirect'] = False
                yield request
            else:
                yield item
            next_page = response.xpath(u'//a[@class="new-nextpage-only"]/@href').extract_first()
            if next_page and page_id <= self.page_limit:
                request = scrapy.Request(url=response.urljoin(next_page), callback=self.parse)
                request.meta['word'] = word
                request.meta['result_id'] = result_id
                request.meta['page_id'] = page_id
                yield request

    def parse_real_url(self, response):
        item = response.meta.get('item')
        html = response.text
        urls = re.findall("location\.replace\(\"(http.*?)\"", html)
        item['show_url'] = response.url
        if urls:
            real_url = urls[0]
            item['show_url'] = real_url

        origin_url = response.xpath(u'//a[contains(text(),"原网站")]/@href').extract_first()
        if origin_url:
            item['show_url'] = origin_url
        yield item

    def get_real_url(self, url):
        # 该函数造成阻塞，速度太慢
        real_url = url
        try:
            r = requests.get(url, allow_redirects=True)
            html = r.content
            urls = re.findall("location\.replace\(\"(.*?)\"", html)
            if urls and 'about:blank' not in urls[0]:
                real_url = urls[0]
        except:
            pass
        return real_url

# -*- coding: utf-8 -*-
import scrapy
import re
from os.path import dirname, join

class BaiduSpider(scrapy.Spider):
    name = "Baidu"
    allowed_domains = ["baidu.com"]

    def __init__(self, words=u"别墅", page_limit=1, **kwargs):
        super(BaiduSpider, self).__init__(self, **kwargs)
        words = words.decode('gbk').encode('utf-8')
        self.words = re.split(u',|;', words)
        self.page_limit = int(page_limit)

    def start_requests(self):
        f = open(join(dirname(__file__), '../../data/word2.csv'))
        for word in f.readlines():
            word = word.strip()
            if not word:
                continue
            url = u"https://www.baidu.com/s?wd=" + word
            yield scrapy.Request(url=url, callback=self.parse, meta={"word": word, "result_id": 0, 'page_id': 1})

    def parse(self, response):
        results = response.xpath('//div[@id="content_left"]/div')
        word = response.meta.get('word', '')
        result_id = response.meta.get('result_id', 0)
        page_id = response.meta.get('page_id', 1)
        page_id += 1
        for result in results:
            hit_top_new = 'hit_top_new' in (result.xpath('./@class') or "")
            if hit_top_new:
                continue
            ad = result.xpath(u'.//a/span[text()="广告"]')
            if ad:
                g_results = result.xpath('./div')
                for g_result in g_results:
                    title = "".join(g_result.xpath('./div[1]//a//text()').extract())
                    url = g_result.xpath('./div[1]//a//@href').extract_first() or ''
                    abstract = "".join(g_result.xpath('./div[2]//a//text()').extract())
                    show_url1 = g_result.xpath('./div[3]//span/text()').extract_first() or ''
                    show_url2 = g_result.xpath('.//div/a/span[contains(text(),".com")]/text()').extract_first() or ''
                    show_url = show_url1 or show_url2
                    is_ad = u"推广"
                    result_id += 1
                    if not all([title, url]):
                        pass
                        # print "="*30
                        # print g_result.extract()
                        # print "="*30
                    yield {'keyword': word,
                            'title': title,
                            'abstract': abstract,
                            'url': url,
                            'show_url': show_url,
                            'is_ad': is_ad}
            else:
                title = "".join(result.xpath('.//h3/a//text()').extract())
                url = result.xpath('.//h3/a/@href').extract_first()
                abstract = "".join(result.xpath('.//div[@class="c-abstract"]//text()').extract())
                show_url1 = result.xpath('.//span[@class="c-showurl"]/text()').extract_first() or ""
                show_url2 = result.xpath('.//a[@class="c-showurl"]/text()').extract_first() or ""
                show_url = show_url1 or show_url2
                is_op = 'result-op' in (result.xpath('./@class').extract_first()  or "")
                is_ad = u""
                if is_op:
                    is_ad = u"OP"
                result_id += 1
                if not all([title, url]):
                    pass
                        # print "="*30
                        # print result.extract()
                        # print "="*30
                yield {'keyword': word,
                       'title': title,
                       'abstract': abstract,
                       'url': url,
                       'show_url': show_url,
                       'is_ad': is_ad}
            next_page = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
            if next_page and page_id <= self.page_limit:
                yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse, meta={'word': word, 'result_id': result_id, 'page_id': page_id})
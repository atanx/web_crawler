# -*- coding: utf-8 -*-
import scrapy
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class LishiSpider(scrapy.Spider):
    name = "Lishi"
    allowed_domains = ["lishichunqiu.com"]

    def start_requests(self):
        menus = [('http://www.lishichunqiu.com/shanggu/', u'上古'),
                 ('http://www.lishichunqiu.com/xiachao/', u'夏朝'),
                 ('http://www.lishichunqiu.com/shangchao/', u'商朝'),
                 ('http://www.lishichunqiu.com/zhouchao/', u'西周'),
                 ('http://www.lishichunqiu.com/chunqiuzhanguo/', u'春秋战国'),
                 ('http://www.lishichunqiu.com/qinchao/', u'秦朝'),
                 ('http://www.lishichunqiu.com/hanchao/', u'汉朝'),
                 ('http://www.lishichunqiu.com/sanguo/', u'三国'),
                 ('http://www.lishichunqiu.com/weijinnanbeichao/', u'魏晋南北朝'),
                 ('http://www.lishichunqiu.com/suichao/', u'隋朝'),
                 ('http://www.lishichunqiu.com/tangchao/', u'唐朝'),
                 ('http://www.lishichunqiu.com/songchao/', u'宋朝'),
                 ('http://www.lishichunqiu.com/yuanchao/', u'元朝'),
                 ('http://www.lishichunqiu.com/mingchao/', u'明朝'),
                 ('http://www.lishichunqiu.com/qingchao/', u'清朝'),
                 ('http://www.lishichunqiu.com/minguo/', u'民国')]
        for m in menus:
            url = m[0]
            dynasty = m[1]
            meta = {'dynasty': dynasty}
            yield scrapy.Request(url, meta=meta, callback=self.parse_menu)

    def parse_menu(self, response):
        # 解析二级目录
        dynasty = response.meta.get('dynasty')
        menus = response.xpath('//div[@id="main-menu-menu"]/a')
        for m in menus:
            url = m.xpath('./@href').extract_first()
            category = m.xpath('./text()').extract_first()
            meta = {'dynasty': dynasty,
                    'category': category}
            yield scrapy.Request(url, callback=self.parse_article_list, meta=meta)

    def parse_article_list(self, response):
        meta = {'dynasty': response.meta.get('dynasty'),
                'category': response.meta.get('category')}

        article_urls = response.xpath('//td[@class="news_list"]/table[@class="box"]//li/a/@href').extract()
        for article_url in article_urls:
            yield scrapy.Request(article_url, callback=self.parse_article, meta=meta)
        next_page = response.xpath(u'//a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_article_list, meta=meta)

    def parse_article(self, response):
        dynasty = response.meta.get('dynasty')
        category = response.meta.get('category')
        content = response.meta.get("content", "")
        title = response.xpath('//h1/text()').extract_first() or ''
        date = _from = author = ''
        info_text = "".join(response.xpath('//td[@class="info_text"]//text()').extract())
        info_text = info_text.replace(u'\xa0', ' ')
        results = re.findall(u'时间：(\d+-\d+-\d+|).*来源：(\S+|).*作者：(\S+|)', info_text)
        if results:
            date, _from, author = results[0]
        ps1 = response.xpath('//td[@id="text"]//p[not(@*)]/text()').extract()
        ps1 = [p for p in ps1 if u"历史春秋网" not in p and not re.findall(u'^[\r\n\u3000 ]+$', p)]
        content1 = "".join(ps1)
        ps2 = response.xpath('//td[@id="text"]//text()').extract()
        ps2 = [p for p in ps2 if u"历史春秋网" not in p and not re.findall(u'^[\r\n\u3000 ]+$', p)]  # 过滤掉干扰文本 "历史春秋网 blablas..."
        content2 = "".join(ps2)
        content += content1 or content2
        tags = ",".join(response.xpath('//a[contains(@href,"tags")]/text()').extract())
        item = {'dynasty': dynasty,
                'category': category,
                'date': date,
                'from': _from,
                'author': author,
                'title': title,
                'content': content,
                'tags': tags}
        next_page = response.xpath(u'//a[contains(text(), "下一页")]/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_article, meta=item)
        else:
            DEBUG = True
            if DEBUG:
                print '===' * 10 + response.url
                print item['dynasty']
                print item['category']
                print item['date']
                print item['from']
                print item['author']
                print item['title']
                print item['content']
                print item['tags']
            yield item

# -*- coding: utf-8 -*-
import scrapy


class AudibleSpider(scrapy.Spider):
	name = "Audible"
	allowed_domains = ["audible.com"]
	start_urls = ('http://www.audible.com/search/',)

	def parse(self, response):
		books = response.xpath('//li[contains(@class, "adbl-result-item")]')
		for book in books:
			# image, title, url, author, narrator, length, date, score
			image = book.xpath('.//img[@class="adbl-prod-image"]/@src').extract_first()
			title = book.xpath('.//div[@class="adbl-prod-title"]/a/text()').extract_first()
			url = (book.xpath('.//div[@class="adbl-prod-title"]//a/@href').extract_first() or '').strip()
			url = response.urljoin(url)
			author = book.xpath('.//div[@class="adbl-prod-meta"]//input[@name="authorName"]/@value').extract()
			author = ';'.join(author)
			narrator = book.xpath('.//a[contains(@href,"searchNarrator")]/text()').extract()
			narrator = ';'.join(narrator)
			length = book.xpath('.//li[contains(./span/text(),"Length")]/span[2]/text()').extract_first() or ''
			release_date = book.xpath('.//li[contains(./span/text(),"Release Date")]/span[2]/text()').extract_first() or ''
			rating = (book.xpath('.//span[@class="boldrating"]/text()').extract_first() or '').strip()
			item = dict()
			item['image'] = image
			item['title'] = title
			item['url'] = url
			item['author'] = author
			item['narrator'] = narrator
			item['length'] = length
			item['release_date'] = release_date
			item['rating'] = rating
			item['image'] = image
			yield item
		next_page = response.xpath('.//span[@class="adbl-page-next"]/a/@href').extract_first()
		if next_page:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
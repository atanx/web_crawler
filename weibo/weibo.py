# coding=utf-8
from selenium import webdriver
import time
import re
import os
import sys
import datetime
from splinter import Browser
from scrapy.selector import Selector

reload(sys)
sys.setdefaultencoding('utf-8')


class Weibo(object):
	"""
	询对象。
	__init__(self)
	"""

	def __init__(self, **kwargs):
		"""
		"""
		self.host = u'http://www.weibo.com'
		self.chrome = None
		self.items = []
		self.delay = kwargs.get('delay', 2)
		self.page_num = kwargs.get('page_num', 5)

	def init_browser(self):
		"""
			初始化浏览器。
			:param driver: 浏览器驱动类型。
			:return: 无
		"""
		self.browser = Browser('chrome')

	def set_login_info(self, username="", password=""):
		"""
		设置登录信息。
		:param username: 用户名称
		:param password: 用户密码
		:return: 无
		"""
		# TODO
		self.u = username
		self.p = password

	def login(self):
		"""
		登录账号。
		:return: 无。
		"""
		login_url = self.host + '/user_login'
		self.browser.visit(login_url)
		self.browser.find_by_xpath('//a[text()="账户登录"]')[0].click()
		self.browser.find_by_id('loginname')[0].value = self.u
		self.browser.find_by_id('nloginpwd')[0].value = self.p
		self.browser.find_by_id('loginsubmit')[0].click()

	def logout(self):
		"""
		退出登录。
		:return: 无
		"""
		assert self.browser is not None, u"浏览器未初始化，使用self.init_browser()初始化浏览器"
		self.browser.visit(self.host + '/user_logout')

	def start_requests(self, url):
		self.browser.visit(url)
		time.sleep(self.delay*2)

	def parse_pages(self):
		"""
		Function to parse item info
		解析字段：
		:keyword
		"""
		time.sleep(self.delay)
		html = self.browser.html
		if u"你的行为有些异常，请输入验证码：" in html:
			a = input(u'输入1继续：')
		next_pages = self.browser.find_by_xpath('//a[contains(@class, "page next")]')
		if not next_pages:
			time.sleep(self.delay)
			next_pages = self.browser.find_by_xpath('//a[contains(@class, "page next")]')
		if not next_pages:
			time.sleep(self.delay)
			next_pages = self.browser.find_by_xpath('//a[contains(@class, "page next")]')
		response = Selector(text=html)
		mblogs = response.xpath('//div[@mid]')
		for mblog in mblogs:
			nickname = mblog.xpath('.//a[@class="W_texta W_fb"]/@nick-name').extract_first()
			content = mblog.xpath('.//p[@class="comment_txt"]//text()').extract()
			content = ''.join(content).strip()
			date_time = mblog.xpath('.//a[@class="W_textb"]/@title').extract_first()
			# favorite = mblog.xpath('.//a[@action-type="feed_list_favorite"]//text()').extract()[-1]
			forward = mblog.xpath('.//a[@action-type="feed_list_forward"]//text()').extract()[-1].replace(u'转发', u'')
			comment = mblog.xpath('.//a[@action-type="feed_list_comment"]//text()').extract()[-1].replace(u'评论', u'')
			like = mblog.xpath('.//a[@action-type="feed_list_like"]//text()').extract_first() or u''
			item = (nickname, content, date_time, forward, comment, like)
			self.items.append(item)
		print "采集数：%d" % len(self.items)
		if next_pages:
			next_page = next_pages[0]
			next_page.click()
			self.parse_pages()

	def to_csv(self, filename, base_path=None):
		"""
		写入txt文件。
		:filename 文件名
		:base_path 文件存储路径
		:return: 无，写入路径
		"""
		if base_path is None:
			filename = os.path.join(os.getcwd(), filename)
		else:
			filename = base_path + filename
		f = open(filename, 'w+')
		# (nickname, content, date_time, forward, comment, like)
		headers = [u'博主',
					u'博文',
					u'日期',
					u'转发数',
					u'评论数',
					u'点赞数']
		header_line = u','.join(headers).encode('gbk', errors='ignore')
		f.write(header_line+'\n')
		for item in self.items:
			item = [i.replace(u',', u';') for i in item]  # csv采用","分割
			line = u','.join(item) + u'\n'
			line = line.encode('gbk', errors='ignore')
			f.write(line)
		f.close()

	def execute(self, **kwargs):
		"""
		:param kwargs:初始化参数
		:return:
		"""
		self.parse_pages()
		filename = kwargs.get('filename') or datetime.datetime.today().strftime('%Y%m%d%H%M%S.csv')
		self.to_csv(filename)


if __name__ == "__main__":
	wb = Weibo(delay=5)
	wb.init_browser()
	a = input('aa:')
	para = [ #('20161203-20170111.csv', 'http://s.weibo.com/weibo/%25E9%259B%25BE%25E9%259C%25BE&typeall=1&suball=1&timescope=custom:2016-12-03:2017-01-11'),
			  ('20160915-20161202.csv', 'http://s.weibo.com/weibo/%25E9%259B%25BE%25E9%259C%25BE&typeall=1&suball=1&timescope=custom:2016-09-15:2016-12-02'),
			('20170112-20170314.csv', 'http://s.weibo.com/weibo/%25E9%259B%25BE%25E9%259C%25BE&typeall=1&suball=1&timescope=custom:2017-01-12:2017-03-14')]
	for filename, url in para:
		wb.start_requests(url)
		wb.execute(delay=5, filename=filename)
		wb.items = []


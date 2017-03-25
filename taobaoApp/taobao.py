# coding=utf-8
from selenium import webdriver
import time
import re
import os
import sys
import datetime

# log_file = datetime.datetime.today().strftime('%Y%m%d.txt')
# log_fid = open(log_file, 'a+')

reload(sys)
sys.setdefaultencoding('utf-8')

'''
class ReadJD(object):
	def __init__(self):
		self.host = 'https://cread.jd.com'
		self.start_url = 'https://cread.jd.com/readbook/readbook_myReadBookList.action'
		self.browser = Browser('chrome')
		self.u = base64.b64decode('MDdqaWFuZ2JpbkAxNjMuY29t')
		self.p = base64.b64decode('d29zaGkxMTAu')
		self.book_list = []

	def login(self):
		self.browser.visit(self.start_url)
		self.browser.find_by_xpath('//a[text()="账户登录"]')[0].click()
		self.browser.find_by_id('loginname')[0].value = self.u
		self.browser.find_by_id('nloginpwd')[0].value = self.p
		self.browser.find_by_id('loginsubmit')[0].click()

	def parse_book_list(self, url):
		if url:
			self.browser.visit(url)
			html = self.browser.html
			s = Selector(text=html)
			urls = s.xpath('//a[@id="btnOnlineRead"]/@href').extract()
			items = [self.host+url for url in urls]
			self.book_list += items
			next_page = ''
			if next_page:
				self.parse_book_list(next_page)

	def crawl_book_list(self):
		self.parse_book_list(self.start_url)

	def crawl_one_book(self, url):
		# 不断向下翻页直到最后
		self.browser.visit(url)
		html_old = ''
		html_new = self.browser.html
		end_flag = (len(html_new) == len(html_old))
		next_page = self.browser.find_by_xpath('//li[@class="changePage_next"]')
		s = Selector(text=self.browser.html)
		pages = s.xpath('//div[@class="JD_page JD_page_show" or @class="JD_page"]').extract()
		title = s.xpath('//title/text()').extract_first()
		filename = re.sub(' |--.*', '', title) + '.html'
		if os.path.exists(filename):
			print(u"%s已存在" % filename)
			return None
		JD_pages = pages
		while next_page and not end_flag:
			for i in range(0, 50):
				next_page[0].click()
				s = Selector(text=self.browser.html)
				pages = s.xpath('//div[@class="JD_page"]').extract()
				for page in pages:
					if page not in JD_pages:
						JD_pages.append(page)
				time.sleep(0.1)
			html_old = html_new
			html_new = self.browser.html
			end_flag = (len(html_new) == len(html_old))
		pages_str = u"".join(JD_pages)
		pages_str = re.sub('width: 573px; height: \d+px', 'width: 675px; height: 770px', pages_str)
		pages_str = re.sub('<div class="JD_page" style="width: 675px;', '<div class="JD_page" style="width: 800px;', pages_str)
		html = template.replace(u'%{content}', pages_str)
		try:
			f = open(filename, 'w+')
			f.write(html)
			print(u"下载《%s》成功。"%title)
		except:
			print(u"写入文件失败")

	def crawl_all_books(self):
		for book in self.book_list:
			self.crawl_one_book(book)
'''


class Taobao(object):
	"""
	企查查查询对象。
	__init__(self)
	"""

	def __init__(self, **kwargs):
		"""
		初始化。
		:param kwargs: 可选参数如下。
		delay: 打开页面后延时，单位：秒
		page_num: 页数
		limits: dict类型，min_viewer, int类型最低人气
							max_viewer, int类型最高人气
							title_exclued， list类型过滤标题中关键词
		"""
		self.host = u'http://www.taobao.com'
		self.chrome = None
		self.items = []
		self.items_filtered = []
		self.delay = kwargs.get('delay', 2)
		self.page_num = kwargs.get('page_num', 5)
		self.limits = kwargs.get('limits', dict())

	def set_param(self, **kwargs):
		self.delay = kwargs.get('delay', 2)
		self.page_num = kwargs.get('page_num', 5)
		self.limits = kwargs.get('limits', dict())

	def init_browser(self):
		"""
		初始化浏览器。
		:param driver: 浏览器驱动类型。
		:return: 无
		"""
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_extension('kdb.crx')
		chrome = webdriver.Chrome(chrome_options=chrome_options)
		self.chrome = chrome
		self.chrome.get(self.host)

	#
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

	def parse_item(self, x):
		"""
		Function to parse item info

		解析字段：
		:keyword
		:price_range
		:location
		:sort_type
		:shopname
		:item_title
		:item_link
		:item_id
		:item_price
		:item_sold_qty
		:online_viewer
		:title_exclued
		"""
		keyword = price_range = location = sort_type = shopname = item_title = item_link = item_id = item_price = item_sold_qty = online_viewer = title_exclued = u''
		try:
			keyword = self.chrome.find_element_by_xpath('//input[@accesskey="s"]').get_attribute('value')
		except:
			pass
		try:
			min_price = self.chrome.find_element_by_xpath(u'//input[@aria-label="价格最小值"]').get_attribute('value')
			max_price = self.chrome.find_element_by_xpath(u'//input[@aria-label="价格最大值"]').get_attribute('value')
			price_range = u'-'.join([min_price, max_price])
		except:
			pass
		try:
			location = self.chrome.find_element_by_xpath(u'//div[@class="inner"]/span').text
		except:
			pass
		try:
			sort_type = self.chrome.find_element_by_xpath('//li[@class="sort"]/a[contains(@class, "active")]').text
		except:
			pass
		try:
			shopname = x.find_element_by_xpath('.//div[contains(@class,"shop")]').text
		except:
			pass
		try:
			item_title = x.find_element_by_xpath('.//div[contains(@class,"title")]').text
		except:
			pass
		try:
			item_link = x.find_element_by_xpath('.//div[contains(@class,"title")]//a').get_attribute('href')
		except:
			pass
		try:
			item_id = x.find_element_by_xpath('.//div[contains(@class,"title")]/a').get_attribute('trace-nid')
		except:
			pass
		try:
			item_price = x.find_element_by_xpath('.//div[contains(@class,"price")]').text
			item_price = item_price.replace(u'\xa5', '')
		except:
			pass
		try:
			item_sold_qty = x.find_element_by_xpath('.//div[contains(@class,"deal-cnt")]').text
			item_sold_qty = re.findall('\d+', item_sold_qty)[0]
		except:
			pass
		try:
			online_viewer = x.find_element_by_xpath('.//span[contains(@class,"dzt-online-viewer")]').text
			online_viewer = re.findall('\d+', online_viewer)[0]
		except:
			online_viewer = 0
			pass
		title_exclued = u';'.join(self.limits.get('title_exclued'))
		item = {
			'keyword': keyword,
			'price_range': price_range,
			'location': location,
			'sort_type': sort_type,
			'shopname': shopname,
			'item_title': item_title,
			'item_link': item_link,
			'item_id': item_id,
			'item_price': item_price,
			'item_sold_qty': item_sold_qty,
			'online_viewer': online_viewer,
			'title_exclued': title_exclued
		}
		return item

	def parse_page(self):
		self.page_num -= 1
		time.sleep(self.delay)
		xs = self.chrome.find_elements_by_xpath('//div[contains(@class,"item J_MouserOnverReq")]')
		for x in xs:
			item = self.parse_item(x)
			if any(item):
				self.items.append(item)

		try:
			next_page = self.chrome.find_element_by_xpath(u'//span[contains(text(),"下一页")]')
		except:
			next_page = None
		if next_page and self.page_num:
			next_page.click()
			time.sleep(self.delay)
			self.parse_page()

	def _filter(self, item):
		"""
		过滤函数, 根据排除内容、online_viewer过滤。
		:return:
		"""
		online_viewer = int(item.get('online_viewer', 0))
		item_title = item.get('item_title', '')
		title_exclued = self.limits.get('title_exclued')
		min_viewer = self.limits.get('min_viewer', 1)
		max_viewer = self.limits.get('max_viewer', 100000000)
		if online_viewer < min_viewer or online_viewer > max_viewer:
			return False
		for ex in title_exclued:
			if ex and ex in item_title:
				return False
		return True

	def filter_item(self):
		"""
		根据条件过滤item
		:return: self.items_filtered
		"""
		self.items_filtered = filter(self._filter, self.items)

	def _auto_filename(self):
		timestamp = datetime.datetime.today().strftime('%Y-%m-%d_%H%M%S')
		if self.items_filtered:
			keyword = self.items_filtered[0].get('keyword').replace(' ', '')
			location = self.items_filtered[0].get('location').replace(' ', '')
		else:
			keyword = u"未知"
			location = u"未知"
		filename = u'_'.join([keyword, location, timestamp + '.csv'])
		return filename

	def to_csv(self, filename, base_path=None):
		"""
		写入txt文件。
		:filename 文件名
		:base_path 文件存储路径
		:return: 无，写入路径
		"""
		if base_path is None:
			filename = os.path.join(os.getcwd(), 'data', filename)
		else:
			filename = base_path + filename
		f = open(filename, 'w+')
		min_viewer = self.limits.get('min_viewer') or ''
		max_viewer = self.limits.get('max_viewer') or ''
		viewer_range = str(min_viewer) + '-' + str(max_viewer)
		headers = [u'关键词',
					u'价格区间',
					u'地址',
					u'排名方式',
					u'店铺旺旺',
					u'宝贝标题',
					u'宝贝链接',
					u'宝贝id',
					u'宝贝价格',
					u'宝贝销量',
					u'在线人数' + viewer_range,
					u'标题排除内容']
		header_line = u','.join(headers).encode('gbk', errors='ignore')
		f.write(header_line + '\n')
		for item in self.items_filtered:
			parts = [item.get('keyword', ''),
					item.get('price_range', ''),
					item.get('location', ''),
					item.get('sort_type', ''),
					item.get('shopname', ''),
					item.get('item_title', ''),
					item.get('item_link', ''),
					item.get('item_id', ''),
					item.get('item_price', ''),
					item.get('item_sold_qty', ''),
					item.get('online_viewer', ''),
					item.get('title_exclued', '')]
			line = u','.join(parts) + u'\n'
			line = line.encode('gbk', errors='ignore')
			f.write(line)
		f.close()

	def execute(self, **kwargs):
		"""
		:param kwargs:初始化参数
		:return:
		"""
		self.set_param(**kwargs)
		self.parse_page()
		self.filter_item()
		filename = kwargs.get('filename') or self._auto_filename()
		self.to_csv(filename)


if __name__ == "__main__":
	tb = Taobao()
	tb.init_browser()
	kw = {'delay': 2,
			'page_num': 5,
			'limits': {'min_viwer': 50,
						'max_viwer': 1000,
						'title_exclued': [u'海鸥', u'卡西欧']}
		}
	tb.execute(**kw)

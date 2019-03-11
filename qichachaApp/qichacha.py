# coding=utf-8
from splinter import Browser
import time
import re
import os
import base64
import sys
import datetime
# from selector import Selector

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

class Qichacha(object):
	"""
	企查查查询对象。
	__init__(self)
	"""
	def __init__(self):
		self.host = u'http://www.qichacha.com'
		self.start_url = u'http://www.qichacha.com/search?key={name}#index:4&'
		self.browser = None
		self.firms = []
		self.emails = []
		self._pages = 0  # 页面计数器

	def init_browser(self, driver=u"chrome"):
		"""
		初始化浏览器。
		:param driver: 浏览器驱动类型。
		:return: 无
		"""
		self.browser = Browser(driver)
		self.browser.visit(self.host)

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

	def _parse_firm_list(self, max_pages):
		"""
		解析一页列表。
		:param url: 链接
		:param max_pages: 最大页数
		:return:
		"""
		max_pages -= 1
		b = self.browser
		trs = b.find_by_xpath('//table[@class="m_srchList"]/tbody//tr')
		# response = Selector(text=browser.html)
		# trs = response.xpath('//table[@class="m_srchList"]/tbody//tr')
		for tr in trs:
			html = tr.outer_html
			urls = re.findall("href=\"(.*?)\"", html)
			# td = tr.xpath('.//a[@class="ma_h1"]')[0]
			# url = td.xpath('./@href').extract_first() or ''
			# html = tr.extract()
			# if u"在业" in html or u"存续" in html:
			# 	url = self.host + urls[0]
			# 	self.firms.append(url)
			if urls and u"在业" in html or u"存续" in html:
				url = self.host + urls[0]
				self.firms.append(url)
		next_page = b.find_by_xpath('//a[@id="ajaxpage" and contains(text(),">")]')
		if next_page and max_pages:
			next_page = next_page[0]
			next_page.click()
			time.sleep(1)
			self._parse_firm_list(max_pages)

	def crawl_firm_list_by_name(self, name=None, max_pages=20):
		"""
		按名称爬取企业列表。
		:param name: string, 法人名称
		:param max_pages: int, 最大爬取页数
		:return: list, 企业链接
		"""
		self.firms = []
		start_url = self.start_url.format(name=name)
		self.browser.visit(start_url)
		self._parse_firm_list(max_pages)

	def parse_one_email(self, url):
		"""
		解析一个页面中的邮箱
		:param url: 页面链接
		:return: 无。解析出的邮箱附加到了self.emails中。
		"""
		self.browser.visit(url)
		elements = self.browser.find_by_xpath(u'//a[contains(text(),"邮箱")]')
		if elements:
			element = elements[0]
			email = element._element.get_attribute('href').replace('mailto:', '')
			self.emails.append(email)
			return email
		else:
			return None

	def parse_all_emails(self, urls):
		"""
		解析一组url中的邮箱。
		:param urls:
		:return:
		"""
		self.emails = []
		for url in urls:
			self.parse_one_email(url)

	def to_text(self, name, base_path=None):
		"""
		写入txt文件。
		:param name: 法人名
		:param base_path: 指定文件路径
		:return: 无，写入路径
		"""
		if base_path is None:
			filename = os.path.join(os.getcwd(), 'data', name + '.txt')
		else:
			filename = base_path + name + '.txt'
		f = open(filename, 'w+')
		for email in self.emails:
			f.write("%s\n" % email)
		f.close()

	def execute(self, name=u'', max_pages=30):
		"""
		爬取指定法人的所有邮箱。
		:param name: 法人名称
		:param max_pages: 最大抓取页数。
		:return:
		"""
		self.crawl_firm_list_by_name(name=name, max_pages=max_pages)
		self.parse_all_emails(self.firms)
		self.to_text(name)

if __name__ == "__main__":
	qcc = Qichacha()
	qcc.init_browser()
	qcc.execute(name=u'马云')
	qcc.execute(name=u'雷军', max_pages=10)

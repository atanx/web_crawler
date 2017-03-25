#!/usr/bin/env python
#coding=utf-8

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_extension('kdb.crx')
chrome = webdriver.Chrome(chrome_options=chrome_options)

chrome.get('www.taobao.com')


xs = chrome.find_elements_by_xpath('//div[contains(@class,"item J_MouserOnverReq")]')
x = xs[0]


def parse_item(x):
	"""Function to parse item info"""
	userid = shop = title = link = price = deal_cnt = online_viewer = u''
	try:
		userid = x.find_element_by_xpath('.//a[contains(@class, "shopname")]').get_attribute('data-userid')
	except:
		pass
	try:
		shop = x.find_element_by_xpath('.//div[contains(@class,"shop")]').text
	except:
		pass
	try:
		title = x.find_element_by_xpath('.//div[contains(@class,"title")]').text
	except:
		pass
	try:
		link = x.find_element_by_xpath('.//div[contains(@class,"title")]//a').get_attribute('href')
	except:
		pass
	try:
		price = x.find_element_by_xpath('.//div[contains(@class,"price")]').text
	except:
		pass
	try:
		deal_cnt = x.find_element_by_xpath('.//div[contains(@class,"deal-cnt")]').text
	except:
		pass
	try:
		online_viewer = x.find_element_by_xpath('.//span[contains(@class,"dzt-online-viewer")]').text
	except:
		pass
	print '\n'.join([userid, shop, title, link, price, deal_cnt, online_viewer])
	return [userid, shop, title, link, price, deal_cnt, online_viewer]

for x in xs:
	parse_item(x)

next_page = chrome.find_element_by_xpath('//a[contains(@class,"J_Ajax")]')

chrome.find_element_by_xpath(u'//span[contains(text(),"下一页")]').click()

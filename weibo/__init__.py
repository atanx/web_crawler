# coding=utf-8

import json
from splinter import Browser
import time
import re

result = []
page_num = 0
browser = Browser("chrome")
KEYWORD = '雾霾'

def parse_one_page(blog_json):
	global result
	try:
		data = json.loads(blog_json)
		mblogs = data['cards'][0]['card_group']
		if mblogs:
			result += mblogs
	except:
		pass


def parse_mblog(mblog, remove_link=True):
	mblog = mblog.get('mblog',dict())
	id = mblog.get('id', '')
	gender = mblog.get('user',dict()).get('gender', '')
	text = mblog.get('text', '')
	if remove_link:
		text = re.sub(u'<a.*</a>', u'', text)
	item = (id, gender, text)
	print '\n'.join(item)
	return item


def login():
	browser.visit("http://m.weibo.cn")


def create_url(page_num):
	url = 'http://m.weibo.cn/container/getIndex?type=all&queryVal={keyword}' \
			'&luicode=10000011&lfid=106003type%3D1&title={keyword}' \
			'&containerid=100103type%3D1%26q%3D%E9%9B%BE%E9%9C%BE' \
			'&page={page_num}'.format(keyword=KEYWORD, page_num=page_num)
	return url


def crawl(MAX_ITEM_COUNT):
	global page_num
	while len(result) < MAX_ITEM_COUNT:
		page_num += 1
		url = create_url(page_num)
		browser.visit(url)
		time.sleep(2)
		pre = browser.find_by_xpath('//pre')
		if pre:
			html = pre[0].text
			parse_one_page(html)
		print "item count: %d" % len(result)



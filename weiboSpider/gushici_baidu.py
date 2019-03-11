#!/usr/bin/env python
# coding=utf-8

import requests
import json
import pickle
import time
import random

class BaiduShici(object):
	headers = {
		'Host': 'hanyu.baidu.com',
		'Referer': 'http://hanyu.baidu.com/s?wd=%E8%AF%97%E8%AF%8D&device=pc&from=home',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
	}

	def __init__(self):
		self.data_file = 'data.gushi'
		self.data_updated = False
		self.load_data()
		self.sesson = requests.Session()

	def today(self):
		return time.strftime('%Y%m%d')

	def _parse(self, response):
		url = response.url
		content = response.content
		o = json.loads(content)
		base_url = 'http://hanyu.baidu.com/shici/detail?pid='
		for each in o['ret_array']:
			body = u''.join(each.get('body', []))
			sid = each['sid'][0]
			display_name = u','.join(each.get('display_name', []))
			dynasty = u','.join(each.get('dynasty', []))
			author = u','.join(each.get('literature_author', []))
			poem_url = base_url + sid
			poem = {
				'body': body,
				'name': display_name,
				'url': poem_url,
				'parent_url': url,
				'dynasty': dynasty,
				'author': author
			}
			self.data[sid] = poem

	def get_page(self, i):
		if i in self.url.get('success'):
			print "已抓取，跳过"
			return
		data_size_before = len(self.data)
		url = 'http://hanyu.baidu.com/hanyu/ajax/search_list?wd=%E8%AF%97%E8%AF%8D&pn=' + str(i)
		try:
			response = self.sesson.get(url, headers=self.headers)
			self._parse(response)
		except:
			pass
		data_size_after = len(self.data)

		# 抓数据失败
		if data_size_before == data_size_after:
			print 'ERR {i}/{total}'.format(i=i, total=self.counter.get('total'))
			self.url['error'][i] = True
			self.sesson = requests.Session()
		else:
			self.data_updated = True
			self.url['success'][i] = data_size_after - data_size_before
			self.url['error'] = {}
			self.url['todo'].pop(i)

	def load_data(self):
		try:
			with open(self.data_file) as fid:
				data = pickle.load(fid)
				self.data = data.get('data')
				self.counter = data.get('counter')
				self.url = data.get('url')
		except IOError:
			self.data = {}
			self.counter = {'total': 12518}
			self.url = {'success': {}, 'error': {}, 'todo': {}}
			for i in range(1, self.counter.get('total') + 1):
				self.url['todo'][i] = True

	def download_data(self):
		todo = self.url['todo'].keys()
		#random.shuffle(todo)
		for i in todo:
			print '{i}/{total} DATA={j}'.format(i=i, total=self.counter.get('total'), j=len(self.data))
			self.get_page(i)
			if len(self.url.get('error')) > 10:
				break

	def dump_data(self):
		if not self.data_updated:
			print "没有新数据"
			return
		self.url['error'] = {}
		data = {
			'data': self.data,
			'counter': self.counter,
			'url': self.url
		}
		with open(self.data_file, 'w+') as fid:
			pickle.dump(data, fid)

	def run(self):
		self.download_data()
		self.dump_data()


if __name__ == '__main__':
	todo = 1
	run_time = 0
	while todo > 0:
		run_time += 1
		print u'第{i}轮'.format(i=run_time)
		bs = BaiduShici()
		bs.run()
		todo = len(bs.url.get('todo'))

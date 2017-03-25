# !/usr/bin/env python
# coding=utf-8

from operator import itemgetter
from itertools import groupby

class DupRemover():
	def __init__(self, csv_file, has_headers=True):
		self.csv_file = csv_file
		self.data = None
		self.result = None
		self.has_headers = has_headers

	def read_csv(self):
		f = open(self.csv_file)
		data = [line.rstrip('\n').split(',')[:5] for line in f.readlines()]
		if self.has_headers:
			self.data = data[1:]
		else:
			self.data = data
		f.close()

	def remove_dup(self):
		# 去重排序
		data = self.data
		data_sorted = sorted(data, key=itemgetter(-1))
		groups = groupby(data_sorted, key=itemgetter(-1))
		result = []
		for label, values in groups:
			values = list(values)
			item = values[0]
			item.append(len(values))
			result.append(item)
		result_sorted = sorted(result, key=itemgetter(-1), reverse=True)
		self.result = result_sorted

	def write_csv(self):
		# data: 数据
		# csv_file 输出文件名
		output_file = self.csv_file[:-3] + 'csv'
		f = open(output_file, 'w+')
		f.write(u','.join([u'关键词', u'标题',u'简介', u'访问链接', u'网站', u'重复次数']).encode('gbk') + '\n')
		for d in self.result:
			d[-1] = str(d[-1])
			f.write(','.join(d) + '\n')

	def execute(self):
		self.read_csv()
		self.remove_dup()
		self.write_csv()

if __name__ == '__main__':
	dr = DupRemover('tianchenghuayuan_m.raw')
	dr.execute()


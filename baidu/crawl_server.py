#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
from itertools import groupby
from operator import itemgetter
from process_csv import DupRemover

reload(sys)
sys.setdefaultencoding('utf-8')


def get_all_need_crawled(_path):
	all_files = [i for i in os.listdir(_path) if i.endswith('.csv')]
	raw_files = [i for i in os.listdir(_path) if i.endswith('.csv') and not i.endswith('_m.csv') and not i.endswith('_pc.csv')]
	need_crawl_files = []
	for raw_file in raw_files:
		m_file = raw_file[:-4] + '_m.csv'
		pc_file = raw_file[:-4] + '_pc.csv'
		if m_file not in all_files:
			need_crawl_files.append('/'.join([_path, raw_file]))
	return need_crawl_files


def crawl(file_list):
	# 检查待爬取文件列表
	for f in file_list:
		pc_file = f[:-4] + '_pc.csv'
		m_file = f[:-4] + '_m.csv'
		# if not os.path.exists(pc_file):
		# 	tmp_file = pc_file[:3] + 'tmp'
		# 	pc_cmd = 'scrapy crawl Baidu -a csv={csv} > {to}'.format(csv=f, to=tmp_file)
		# 	os.system(pc_cmd)
		# 	rename_cmd = 'ren "{tmp_file}" "{pc_file}"'.format(tmp_file=tmp_file, pc_file=pc_file)
		# 	os.system(rename_cmd)
		if not os.path.exists(m_file):
			tmp_file = m_file[:-3] + 'tmp'
			cmd_m = 'scrapy crawl MobileBaidu -a csv={csv} > {to}'.format(csv=f, to=tmp_file)
			os.system(cmd_m)
			r = DupRemover(tmp_file)  # 去重工具，根据真实网址统计重复数并去重。
			r.execute()
			# rename_cmd = 'ren "{tmp_file}" "{m_file}"'.format(tmp_file=tmp_file, m_file=m_file)
			# os.system(rename_cmd)


if __name__ == "__main__":
	while True:
		cwd = os.path.abspath(os.path.dirname(__file__))
		_path = os.path.join(cwd, '..', 'uPhone', 'static', 'data')
		_path = os.path.abspath(_path)
		file_list = get_all_need_crawled(_path)
		os.chdir(cwd)
		DEBUG = False
		if DEBUG:
			for f in file_list:
				print f
		time.sleep(2)
		print("当前待爬取文件数: %d" % len(file_list))
		for f in file_list:
			print("\t %s" % f)
		crawl(file_list)
		time.sleep(2)




#!/usr/bin/env python
# coding=utf-8

import os
import sys
import time
from itertools import groupby
from operator import itemgetter
from process_csv import DupRemover
from CrawlWeb.config import Config
import sqlite3
import platform
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')

config = Config()
db_file = config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///','')


def query_sites(raw_file):
	if "Windows" in platform.platform():
		raw_file = raw_file.decode('gbk')
		conn = sqlite3.connect(db_file)
	else:
		conn = MySQLdb.connect(host='172.16.0.30',
							   port=3306,
							   user='root',
							   passwd='root',
							   db='spider',
							   charset='utf8')
	sql = u'''SELECT t2.site_list
			from CrawlTask t1 LEFT JOIN Site t2
			on t1.site_id=t2.id
			where t1.raw_file = "{raw_file}"'''.format(raw_file=raw_file)
	curs = conn.cursor()
	curs.execute(sql)
	data = curs.fetchall()
	curs.close()
	conn.close()
	if data:
		site_list = data[0][0] or ''
		return u'#'.join(site_list.split('\n'))
	else:
		return u''

def get_all_need_crawled(_path):
	all_files = [i for i in os.listdir(_path) if i.endswith('.csv')]
	raw_files = [i for i in os.listdir(_path) if
				 i.endswith('.txt') or
				 i.endswith('.csv') and not i.endswith('_m.csv') and not i.endswith('_pc.csv')]
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
		site_list = ''
		file_name = os.path.split(f)[-1]
		site_list = query_sites(file_name)
		print site_list
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
			cmd_m = 'scrapy crawl MobileBaidu -a csv={csv} -a sites="{site_list}"> {to}'.format(csv=f,
																		to=tmp_file,
																		site_list=site_list)
			os.system(cmd_m)
			r = DupRemover(tmp_file)  # 去重工具，根据真实网址统计重复数并去重。
			r.execute()
		# rename_cmd = 'ren "{tmp_file}" "{m_file}"'.format(tmp_file=tmp_file, m_file=m_file)
		# os.system(rename_cmd)


if __name__ == "__main__":
	cwd = os.path.abspath(os.path.dirname(__file__))
	RAW_FILE_PATH = os.path.join(cwd, 'uPhone', 'static', 'data')
	RAW_FILE_PATH = os.path.abspath(RAW_FILE_PATH)
	SPIDER_URI = cwd + '/baidu'
	os.chdir(SPIDER_URI)
	while True:
		file_list = get_all_need_crawled(RAW_FILE_PATH)
		DEBUG = False
		if DEBUG:
			for f in file_list:
				print f
		time.sleep(2)
		print(u"当前待爬取文件数: %d" % len(file_list))
		for f in file_list:
			print("\t %s" % f)
		crawl(file_list)
		time.sleep(2)

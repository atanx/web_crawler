#!/usr/bin/env python
#coding=utf-8

from lianjia import ershoufang as fang


f = fang.get_village_detail2()

districts = ['songjiang', 'qingpu']
# districts = ['qingpu']

for d in districts:
	s = fang.getPlatesByDistrict(d)
	csvFile = './data/' + d + '.csv'
	villages = fang.crawlByDistrict(d)
	df = fang.to_dataframe(villages)
	df.to_csv(csvFile, encoding='gbk')


print "ok"

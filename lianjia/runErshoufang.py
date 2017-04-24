#!/usr/bin/env python
# coding=utf-8

from lianjia import ershoufang

lat = 31.1782420000
long = 121.3778560000
r = 1000  # 半径1000米
csvFileName = 'test.csv'
villages = ershoufang.crawl(lat=lat, long=long, radius=r)
df = ershoufang.to_dataframe(villages)
df.to_csv(csvFileName, encoding='gbk')





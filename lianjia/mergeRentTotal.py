#!/usr/bin/env python
# coding=utf-8

from lianjia import zufang
import os
import sys
import pandas as pd
import numpy as np

sys.path.append('C:\\Users\\youxiang\\PycharmProjects\\web_crawler\\lianjia')

lat = 31.1782420000
long = 121.3778560000
r = 5000  # 半径1000米
xiaoquList = zufang.crawlQuyuList(lat, long, r)
xqDf = pd.DataFrame.from_dict(xiaoquList)
xqDf.index = [int(dataId) for dataId in xqDf.dataId]
rtDf = xqDf[['rentTotal']]

df = pd.DataFrame.from_csv(u'周边小区.csv', encoding='gbk')
fullDf = pd.concat([df, rtDf], axis=1)
finalDf = fullDf[fullDf['showName'].notnull()]
finalDf.to_csv(u'+在租数.csv', encoding='gbk')

finalDf.insert(len(finalDf.columns), u'1室房租均价', np.nan)
total = len(finalDf.index)
for idx, dataId in enumerate(finalDf.index):
	dataIdStr = str(dataId)
	AvgPrice = zufang.crawlAvgRent(dataIdStr)
	finalDf.loc[dataId, [u'1室房租均价']] = AvgPrice
	print u'正在处理{idx}/{length}'.format(idx=idx, length=total)

finalDf.to_csv(u'+在租价格.csv', encoding='gbk')

for i in range(1000):
	print u'正在处理{idx}/880'.format(idx=i)
	time.sleep(1)


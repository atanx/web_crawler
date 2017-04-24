#!/usr/bin/env python
# coding=utf-8
import sys
import pandas as pd
import numpy as np
from lianjia import zufang, ershoufang

sys.path.append('C:\\Users\\youxiang\\PycharmProjects\\web_crawler\\lianjia')

lat = 31.1782420000
long = 121.3778560000
r = 5000  # 半径1000米

# 租房数
villages = ershoufang.crawl(lat, long, r)
df = ershoufang.to_dataframe(villages)
df.index = df.dataId

# 获取租房小区房源数
xiaoquList = zufang.crawlQuyuList(lat, long, r)
xqDf = pd.DataFrame.from_dict(xiaoquList)
xqDf.index = xqDf.dataId
xqDf.insert(len(xqDf.columns), u'1室房租均价', np.nan)
xqDf.insert(len(xqDf.columns), u'2室房租均价', np.nan)
xqDf.insert(len(xqDf.columns), u'3室房租均价', np.nan)
total = len(xqDf.index)
for idx, dataId in enumerate(xqDf.index):
	dataIdStr = str(dataId)
	AvgPrice = zufang.crawlAvgRent(dataIdStr)
	xqDf.loc[dataId, [u'1室房租均价']] = AvgPrice[1]
	xqDf.loc[dataId, [u'2室房租均价']] = AvgPrice[2]
	xqDf.loc[dataId, [u'3室房租均价']] = AvgPrice[3]
	print u'正在处理{idx}/{length}'.format(idx=idx, length=total)
rtDf = xqDf[['rentTotal', u'1室房租均价', u'2室房租均价', u'3室房租均价']]

fullDf = df.join(rtDf)
fullDf.to_csv(u'5公里内小区二手房价格和租房价格.csv', encoding='gbk')

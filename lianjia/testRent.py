#!/usr/bin/env python
# coding=utf-8

from lianjia import zufang
import os
import sys
import pandas as pd

sys.path.append('C:\\Users\\youxiang\\PycharmProjects\\web_crawler\\lianjia')


# 抓取指定小区的租房房源
dataId = '5011000002238'
houseList = zufang.crawlHouseList(dataId)


# 抓取指定半径内的小区列表
lat = 31.1782420000
long = 121.3778560000
r = 5000  # 半径1000米
xiaoquList = zufang.crawlQuyuList(lat, long, r)


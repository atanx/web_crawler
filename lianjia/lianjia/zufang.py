#!/usr/bin/env python
# coding=utf-8
import json

import requests
import numpy as np
from .distance import calc_bounds
from collections import defaultdict

rentQuyuListApi = 'http://soa.dooioo.com/api/v4/online/house/rent/listMapResult?access_token=7poanTTBCymmgE0FOn1oKp&client=pc&cityCode=sh&type=village&minLatitude={minLat}&maxLatitude={maxLat}&minLongitude={minLong}&maxLongitude={maxLong}&siteType=quyu'
rentHouseListApi = 'http://soa.dooioo.com/api/v4/online/rent/zufang/search?access_token=7poanTTBCymmgE0FOn1oKp&client=pc&cityCode=sh&community_id={dataId}&limit_offset=1&limit_count=1000'


def getQuyuListUrl(lat, long, r):
	minLat, maxLat, minLong, maxLong = calc_bounds(lat, long, r)
	url = rentQuyuListApi.format(minLat=minLat, maxLat=maxLat, minLong=minLong, maxLong=maxLong)
	return url


def getHouseListUrl(dataId):
	url = rentHouseListApi.format(dataId=dataId)
	return url


def crawlQuyuList(lat, long, r):
	url = getQuyuListUrl(lat, long, r)
	content = requests.get(url).content
	data = json.loads(content)
	return data['dataList']


def crawlHouseList(dataId):
	url = getHouseListUrl(dataId)
	content = requests.get(url).content
	houseList = json.loads(content)
	return houseList['data']['list']


def crawlAvgRent(dataId):
	rooms = [1, 2, 3]
	avgPrices = dict()
	houseList = crawlHouseList(dataId)
	for room in rooms:
		prices = [house['rentPrice'] for house in houseList if house['room'] == room]
		if any(prices):
			avgPrices[room] = np.average(prices)
		else:
			avgPrices[room] = np.nan
	return avgPrices

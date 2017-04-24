#!/usr/bin/env python
# coding=utf-8
import re
import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

from . import distance

urlDict = {
	'listMapResult': 'http://soa.dooioo.com/api/v4/online/house/ershoufang/listMapResult?',
	'village_detail': 'http://m.sh.lianjia.com/xiaoqu/{dataId}.html',
	'gotoMap': 'http://m.sh.lianjia.com/map/pos?pos={long},{lat}'}


# 拼接API链接
def gen_url(**kwargs):
	url = urlDict['listMapResult']
	# 参数名			, 参数值
	args = [('access_token', kwargs.get('token')),
			('client', kwargs.get('client', 'pc')),
			('cityCode', kwargs.get('city', 'sh')),
			('type', kwargs.get('type', 'village')),
			('minLatitude', kwargs.get('minLat')),
			('maxLatitude', kwargs.get('maxLat')),
			('minLongitude', kwargs.get('minLong')),
			('maxLongitude', kwargs.get('maxLong')),
			('siteType', kwargs.get('siteType', 'quyu'))]
	argStr = '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in args])
	url += argStr
	return url


# 获取指定位置的周边小区
def get_villages(url):
	html = requests.get(url).content
	responseDict = json.loads(html)
	villages = responseDict['dataList']
	return villages

# 指定小区dataId, 爬取楼栋数、户数、建成年代
# 补充：板块
def get_village_detail(dataId=u'5011000018313'):
	url = urlDict['village_detail'].format(dataId=dataId)
	html = requests.get(url).content
	sp = bs(html, 'html.parser')
	infoText = sp.find('div', attrs={'class': 'p-list'}).text
	bankuaiText = sp.find('a', attrs={'class': 'gotomap'}).text

	details = dict()
	reg = [('buildingCnt', u'(\d+)栋', infoText, 0, ''),
		   ('houseCnt', u'(\d+)户', infoText, 0, ''),
		   ('age', u'(\d+)年', infoText, 0, ''),
		   ('district', u'位置及周边：\[(.*?)\]', bankuaiText, 0, ''),
		   ('region', u'位置及周边：\[.*?\](\S+)', bankuaiText, 0, '')
		   ]

	for key, pattern, string, idx, default in reg:
		try:
			details[key] = re.findall(pattern, string)[idx]
		except:
			details[key] = default
	return details

# 爬取
def crawl(lat, long, radius):
	bounds = distance.calc_bounds(lat, long, radius)
	kwargs = dict(token='7poanTTBCymmgE0FOn1oKp',
				  city='sh',
				  minLat=bounds[0],
				  maxLat=bounds[1],
				  minLong=bounds[2],
				  maxLong=bounds[3])
	mapCenterUrl = gen_url(**kwargs)
	# 所有小区
	villages = get_villages(mapCenterUrl)
	totalCnt = len(villages)
	# 更新小区详情，距离
	for idx, village in enumerate(villages):
		if village.get('distance'):
			continue
		time.sleep(0.2)
		dataId = village.get('dataId')
		villageLat = village.get('latitude')
		villageLong = village.get('longitude')
		villageDetails = get_village_detail(dataId)
		villageDetails['distance'] = distance.calc_distance(lat, long, villageLat, villageLong)
		villageDetails['detailUrl'] = urlDict['village_detail'].format(dataId=dataId)
		villageDetails['gotoMap'] = urlDict['gotoMap'].format(long=villageLong, lat=villageLat)
		village.update(villageDetails)
		print(u'当前进度{idx}/{totalCnt}'.format(idx=idx + 1, totalCnt=totalCnt))
	return villages


def to_dataframe(villages):
	df = pd.DataFrame.from_dict(villages)
	columns = [u'dataId', u'distance', u'showName', u'age', u'buildingCnt', u'houseCnt',
			   u'district', u'region', u'dealAvgPrice', u'saleAvgPrice', u'saleTotal',
			   u'latitude', u'longitude', u'detailUrl', u'gotoMap']

	newColumnNames = {u'dataId': u'dataId',
					  u'distance': u'距离（米）',
					  u'showName': u'小区名称',
					  u'age': u'建成年代',
					  u'buildingCnt': u'楼栋数',
					  u'houseCnt': u'总户数',
					  u'district': u'区县',
					  u'region': u'板块',
					  u'dealAvgPrice': u'成交均价（元）',
					  u'saleAvgPrice': u'在售均价（元）',
					  u'saleTotal': u'在售套数',
					  u'latitude': u'百度地图纬度',
					  u'longitude': u'百度地图经度',
					  u'detailUrl': u'详情页链接',
					  u'gotoMap': u'地图链接'}

	newDf = df.ix[:, columns]
	newDf.rename(columns=newColumnNames, inplace=True)
	return newDf


if __name__ == '__main__':
	lat = 31.1782420000
	long = 121.3778560000
	r = 1000
	csvFileName = 'data.csv'
	villages = crawl(lat=lat, long=long, radius=r)
	df = pd.DataFrame.from_dict(villages)
	df.to_csv(csvFileName, encoding='gbk')

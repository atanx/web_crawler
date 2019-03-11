#!/usr/bin/env python
# coding=utf-8

import re
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


prefix = 'http://sh.lianjia.com'


def parseHouseList(url):
	html = requests.get(url).content
	sp = bs(html, 'html.parser')
	links = sp.find_all('a', attrs={'gahref': re.compile('results_click_order')})
	results = []
	for link in links:
		href = prefix + link.get('href')
		results.append(href)
	return results


def parseDistrictUrl(houseUrl):
	html = requests.get(houseUrl).content
	sp = bs(html, 'html.parser')
	a = sp.find('a', attrs={'gahref': re.compile('^ershoufang')})
	districtUrl = prefix + a.get('href')
	return districtUrl


def get_village_detail(url):
	html = requests.get(url).content
	sp = bs(html, 'html.parser')
	infoText = sp.find('div', attrs={'class': 'summary'}).text

	details = dict()
	reg = [('buildingCnt', u'(\d+)栋', infoText, 0, ''),
		   ('houseCnt', u'(\d+)户', infoText, 0, ''),
		   ('age', u'(\d+)年', infoText, 0, '')
		   ]

	for key, pattern, string, idx, default in reg:
		try:
			details[key] = re.findall(pattern, string)[idx]
		except:
			details[key] = default
	return details


def parseDistrict(districtUrl):
	mobileDistrictUrl = districtUrl.replace('sh','m.sh')
	html = requests.get(districtUrl).content
	sp = bs(html, 'html.parser')

	# 解析名称、地址、类型、户数
	name = address = _type = None
	# 名称
	name = sp.find('h1').text
	# 地址
	address = sp.find('span', attrs={'class': 'adr'}).text
	# 类型
	div = sp.find("div", attrs={'class': 'col-2 clearfix'})
	matches = re.findall(u'物业类型：\s*(.*?)\n', div.text)
	if matches:
		_type = matches[0]
	# 小区户数
	mobileDetails = get_village_detail(mobileDistrictUrl)
	data = {'name': name,
			'address': address,
			'type': _type,
			'houseCnt': mobileDetails.get('houseCnt', None)
			}
	return data


def test():
	districtUrl = 'http://sh.lianjia.com/xiaoqu/5011000009412.html'
	info = parseDistrict(districtUrl)

def main():
	# 房源列表页 -> 房源详情页 -> 楼盘详情页
	basUrl = 'http://sh.lianjia.com/ershoufang/yangpu/b500to1000d'
	urls = [basUrl + str(i) for i in range(1, 58)]
	houseUrls = []
	districtUrls = set()
	districts = []
	for idx, url in enumerate(urls):
		onePageHouseUrls = parseHouseList(url)
		houseUrls.extend(onePageHouseUrls)
		print u'{idx}/{totalCnt}: 解析{url}'.format(idx=idx+1,
												  totalCnt= len(urls),
												  url=url)

	for idx, houseUrl in enumerate(houseUrls):
		districtUrl = parseDistrictUrl(houseUrl)
		districtUrls.add(districtUrl)
		print u'{idx}/{totalCnt}: 解析{url}'.format(idx=idx+1,
											 totalCnt=len(houseUrls),
											 url=houseUrl)

	for idx, districtUrl in enumerate(districtUrls):
		if 'http' not in districtUrl:
			districtUrl = prefix + districtUrl
		district = parseDistrict(districtUrl)
		districts.append(district)
		print u'{idx}/{totalCnt}: 解析{url}'.format(idx=idx+1,
											 totalCnt=len(districtUrls),
											 url=districtUrl)

	df = pd.DataFrame.from_dict(districts)
	df.to_csv('yangpu.csv')


if __name__ =='__main__':
	test()

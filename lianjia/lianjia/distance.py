#!/usr/bin/env python
# coding=utf-8
import math


def calc_bounds(lat, long, r):
	# 经度每隔0.00001度，距离相差约1米
	# 纬度每隔0.00001度，距离相差约1.1米
	minLat = lat - 0.00001 * r
	maxLat = lat + 0.00001 * r
	minLong = long - 0.00001 * r / 1.1
	maxLong = long + 0.00001 * r / 1.1
	return minLat, maxLat, minLong, maxLong


def calc_distance(lat1, long1, lat2, long2):
	dx = abs(lat1 - lat2) / 0.00001 * 1
	dy = abs(long1 - long2) / 0.00001 * 1.1
	d = math.sqrt(dx ** 2 + dy ** 2)
	return d



#!/usr/bin/env python
#coding=utf-8

import MySQLdb
import json

conn = MySQLdb.connect(host='172.16.0.15',
									port=3306,
									user='root',
									passwd='YouxiangWangluo,6',
									db='plus_spider_resultdb',
									charset="utf8")
sql = '''
select task_id, result from plus_spider_resultdb.weibo;
'''
cur = conn.cursor()
cur.execute(sql)
data = cur.fetchall()

data2 = []
for task_id, result in data:
	obj = json.loads(result)
	username = obj.get('username')
	mid = obj.get('mid')
	feed_time = '2017-10-27 17:00'
	data2.append((username, mid, feed_time, task_id))


sql2 = '''
update weibo set username=%s, mid=%s, feed_time=%s where task_id=%s;
'''

cur.executemany(sql2, data2)

conn.commit()



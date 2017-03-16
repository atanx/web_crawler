#!/usr/bin/env python
# coding=utf-8
from . import db


class Site(db.Model):
	__tablename__ = 'Site'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False, unique=True)
	site_list = db.Column(db.String, nullable=True)

	@staticmethod
	def seed():
		sites = [u'site:anjuke.com',
					u'site:fang.com',
					u'site:fangdd.com',
					u'site:focus.cn',
					u'site:house.163.com',
					u'site:house.qq.com',
					u'site:house365.com',
					u'site:jiwu.com',
					u'site:leju.com']
		s = Site(name=u'新房组', site_list=u'\n'.join(sites))
		db.session.add(s)
		db.session.commit()


class CrawlTask(db.Model):
	__tablename__ = "CrawlTask"
	id = db.Column(db.Integer, primary_key=True)
	raw_file = db.Column(db.String, nullable=False, unique=True)
	m_file = db.Column(db.String, nullable=True)
	site_id = db.Column(db.Integer)


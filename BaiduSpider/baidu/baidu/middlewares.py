#!/usr/bin/env python
#coding=utf-8

from proxy import PROXY_CYCLE

# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64
# Start your middleware class
class ProxyMiddleware(object):
	# overwrite process request
	def __init__(self):
		super(ProxyMiddleware, self).__init__(self)
		self.count = 0
		self.proxy = PROXY_CYCLE.next()

	def change_proxy(self):
		self.count += 1
		if self.count % 200:
			self.proxy = 'https://' + PROXY_CYCLE.next()

	def process_request(self, request, spider):
		request.meta['proxy'] = self.proxy

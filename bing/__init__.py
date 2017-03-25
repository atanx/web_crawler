#!/usr/bin/env python
#coding=utf-8

import requests
from bs4 import BeautifulSoup as bs

url = 'http://global.bing.com/search?q=%E6%A5%BC%E7%9B%98'
html = requests.get(url).content

print html

sp = bs(html, markup='html_parser')


from selenium import webdriver
url = 'http://global.bing.com/search?q=%E6%A5%BC%E7%9B%98'
chrome = webdriver.Chrome()
chrome.get(url)

next_page = chrome.find_element_by_xpath('//a[@class="sb_pagN"]')
next_page.click()

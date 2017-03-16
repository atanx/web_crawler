#utf-8

import urllib
import os
from os.path import dirname,join


def download_image(img_url):
	parts = img_url.split('/')
	name = parts[-1]
	folder = parts[-2]
	to_folder = dirname(__file__) + '/data/' + folder
	if not os.path.exists(to_folder):
		os.mkdir(to_folder)
	to_file = join(to_folder, name)
	urllib.urlretrieve(img_url, to_file)


def get_book(base_path, page_count):
	for i in range(1, page_count+1):
		img_url = base_path + str(i).zfill(3)+'.jpg'
		download_image(img_url)


if __name__ == '__main__':
	base_path = 'http://auto.tom61.com/f/yshb/002/RJC5SXX/'
	get_book(base_path, 145)

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3

class LishichunqiuPipeline(object):
    def start_spider(self):
        conn = sqlite3.connect('')

    def process_item(self, item, spider):

        return item

    def close_spider(self):
        pass

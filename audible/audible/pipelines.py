# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

class PrintPipeline(object):
    def process_item(self, item, spider):
        fields = ['title',
                  'author',
                  'narrator',
                  'length',
                  'release_date',
                  'rating',
                  'image',
                  'url']
        values = []
        for field in fields:
            values.append(item[field])
        print "\t".join(values)
        return item

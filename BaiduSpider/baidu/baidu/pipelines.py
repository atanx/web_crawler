# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class BaiduPipeline(object):
    def __init__(self):
        super(BaiduPipeline, self).__init__()
        print u'关键词,标题,简介,访问链接,网站,推广'.encode('gbk')

    def process_item(self, item, spider):
        keys = ('keyword',
                'title',
                'abstract',
                'url',
                'show_url',
                'is_ad')
        str_item = []
        for key in keys:
            field = item.get(key, '').strip()
            if len(field) > 50 and key == 'title':
                field = field[0:50]
            field = field.replace(',', ';')
            if isinstance(field, str):
                pass
                # field = field.decode('gbk')
            str_item.append(field)
        str_item = u','.join(str_item)
        print str_item.decode('utf-8').encode('gbk', errors='ignore')
        return item

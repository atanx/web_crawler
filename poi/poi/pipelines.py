# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class PrintPipeline(object):
    def process_item(self, item, spider):
        parts = [item.get('name', ''),
                item.get('url', ''),
                item.get('address', ''),
                item.get('phone', ''),
                item.get('district', ''),
                item.get('district_url')]
        print u'#'.join(parts)
        return item

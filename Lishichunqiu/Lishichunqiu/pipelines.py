# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import sqlite3

reload(sys)
sys.setdefaultencoding('utf-8')


class ToDBPipeline(object):
    def __init__(self):
        self.conn = None
        self.curs = None

     def open_spider(self, spider):
        conn = sqlite3.connect('C:\Users\youxiang\PycharmProjects\web_crawler\Lishichunqiu\history.db')
        curs = conn.cursor()
        self.conn = conn
        self.curs = curs

    def process_item(self, item, spider):
        dynasty = item.get('dynasty')
        category = item.get('category')
        date = item.get('date')
        source = item.get('from')
        author = item.get('author')
        title = item.get('title')
        content = item.get('content')
        tags = item.get('tags')
        record = (dynasty, category, date, source, author, title, content, tags)
        sql = u'''
              insert into history("dynasty", "category", "date", "source","author", "title", "content", "tags")
              values(?,?,?,?,?,?,?,?)
              '''
        self.curs.execute(sql, record)
        self.conn.commit()

    def close_spider(self, spider):
        self.curs.close()
        self.conn.close()
        #self.curs.close()
        #self.conn.close()

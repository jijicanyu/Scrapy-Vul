# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
import redis
from scrapy.exceptions import DropItem
from scrapy.conf import settings

Redis = redis.StrictRedis(host='localhost', port=6379, db=0)

class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('vul_title:%s' % item['vul_title']):
            raise DropItem('Duplicate item found: %s' % item)
        else:
            Redis.set('vul_title:%s' % item['vul_title'], 1)
            return item

class ExDbSpiderPipeline(object):
    filename = 'exploitalert.sqlite'
                          
    def __init__(self):
        self.conn=None
        dispatcher.connect(self.initialize,signals.engine_started) 
        dispatcher.connect(self.finalize,signals.engine_stopped)

    def process_item(self,item,spider):
        self.conn.execute('insert into exdb values(?,?,?,?,?,?,?,?,?)',(None,item['edb_id'],item['ref_id'],item['level'],item['vul_score'],item['vul_type'],item['vul_title'],item['vul_detail'],item['vul_author'],item['vul_poc'],item['vul_fixurl'],item['vul_fix'],item['vul_ref'],item['application'],item['app_ver'],item['from_site'],item['public_time'],item['grab_time'],item['vul_access'],item['snapshot']))
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn=sqlite3.connect(self.filename)
        else:
            self.conn=self.create_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn=None

    def create_table(self,filename):
        conn=sqlite3.connect(filename)
        conn.execute("""create table exdb(id integer primary key autoincrement,edb_id text,edb_author text,edb_date text, edb_type text, edb_platform text, edb_title text, edb_cve text, edb_exp text)""")
        conn.commit()
        return conn

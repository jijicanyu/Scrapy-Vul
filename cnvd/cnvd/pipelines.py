# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class CnvdPipeline(object):
#     def process_item(self, item, spider):
#         return item
import sqlite3
from os import path
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

import redis
from scrapy.exceptions import DropItem
from scrapy.conf import settings
import time

Redis = redis.StrictRedis(host='localhost', port=6379, db=0)

class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('CNVD_ID:%s' % item['CNVD_ID']):
            raise DropItem('Duplicate item found: %s' % item)
        else:
            Redis.set('CNVD_ID:%s' % item['CNVD_ID'], 1)
            return item

class CnvdPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    filename = 'cnvd.sqlite'
                          
    def __init__(self):
        self.conn=None
        dispatcher.connect(self.initialize,signals.engine_started)
        dispatcher.connect(self.finalize,signals.engine_stopped)

    def process_item(self,item,spider):
    	print '------------insert---------'
    	print item['title']
        #insert the infomatinon that we can get in the website
        self.conn.execute('insert into exdb values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                (None,#(必)漏洞id atuo increase 
                item['CNVD_ID'],#来源漏洞id
                item['level'],#漏洞等级
                None,#漏洞评分
                None,#漏洞类型
                item['title'],#(必)漏洞标题
                item['cave_desc'],#漏洞详情
                item['auther'],#漏洞发现者
                None,#漏洞验证poc
                item['buding'],#修补引用链接
                item['means'],#修补建议
                item['look_link'],#漏洞参考链接
                item['effect_production'],#影响产品
                None,#产品版本号
                'www.cnvd.org.cn',#(必)来源网站
                item['url'],#(必)来源网址
                item['product_date'],#公开时间
                time.strftime("%Y-%m-%d"),#(必)抓取时间
                None,#攻击方式
                item['snapshot']#(必)快照
                ))
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
        # all the column is 20
        conn.execute("""
            create table exdb(
                id integer primary key autoincrement,
                ref_id text,
                level text,
                vul_score text,
                vul_type text,
                vul_title text,
                vul_detail text,
                vul_author text,
                vul_poc text,
                vul_fixurl text,
                vul_fix text,
                vul_ref text,
                application text,
                app_ver text,
                from_site text,
                from_url text,
                public_time text,
                grab_time text,
                vul_access text,
                snapshot text)""") 
        conn.commit()
        return conn

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class ExDbSpiderItem(Item):
    edb_id = Field()
    edb_author = Field()
    edb_date = Field()
    edb_type = Field()
    edb_platform = Field()
    edb_title = Field()
    edb_cve = Field()
    edb_exp = Field()
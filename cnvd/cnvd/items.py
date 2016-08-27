# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnvdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    title =scrapy.Field()
    CNVD_ID = scrapy.Field()
    product_date = scrapy.Field()
    level = scrapy.Field()
    effect_production =scrapy.Field()
    bugtraq_id = scrapy.Field()
    cave_desc = scrapy.Field()
    look_link = scrapy.Field()
    means = scrapy.Field()
    auther=scrapy.Field()
    buding = scrapy.Field()
    pinfo = scrapy.Field()
    report_date = scrapy.Field()
    collect_date = scrapy.Field()
    update_date = scrapy.Field()
    cave_flie = scrapy.Field()

    url = scrapy.Field()
    snapshot = scrapy.Field()

    else_id = scrapy.Field()

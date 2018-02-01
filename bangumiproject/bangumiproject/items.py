# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class node_imfor(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    chinese_name = scrapy.Field()
    japanese_name = scrapy.Field()
    score = scrapy.Field()
    detail = scrapy.Field()
    rank = scrapy.Field()
    node_url = scrapy.Field()

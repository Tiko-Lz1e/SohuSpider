# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 爬虫获取数据结构
class sohuItem(scrapy.Item):
    collection = "News"
    title = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()
    channel = scrapy.Field()
    author = scrapy.Field()
    personalPage = scrapy.Field()
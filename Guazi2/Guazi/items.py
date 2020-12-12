# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 汽车的名称、价格、链接
    # 第一步
    name = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
    # 行驶里程、排量、变速箱
    km = scrapy.Field()
    displacement = scrapy.Field()
    typ = scrapy.Field()

# 相当于定义了一个字典，只给了key，没有给value
# {'name':'','price':'','link':''}

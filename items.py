# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    district = scrapy.Field()
    county = scrapy.Field()
    rent = scrapy.Field()
    bed = scrapy.Field()
    bath = scrapy.Field()
    area = scrapy.Field()
    special1 = scrapy.Field()
    special2 = scrapy.Field()
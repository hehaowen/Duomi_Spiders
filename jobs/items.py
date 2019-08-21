# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobsItem(scrapy.Item):
    # define the fields for your item here like:
    area = scrapy.Field()
    title = scrapy.Field()
    wage = scrapy.Field()
    details = scrapy.Field()
    settlement = scrapy.Field()
    sort = scrapy.Field()
    people = scrapy.Field()
    company = scrapy.Field()
    introduction = scrapy.Field()

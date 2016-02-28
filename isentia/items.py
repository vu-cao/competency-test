# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    domain = scrapy.Field()
    link = scrapy.Field()
    headline = scrapy.Field()
    article = scrapy.Field()

    date = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    introduction = scrapy.Field()
    category = scrapy.Field()


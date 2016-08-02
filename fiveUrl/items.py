# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FiveurlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    netloc = scrapy.Field()
    from_netloc = scrapy.Field()
    pass

class UrlInjection(scrapy.Item):
    url = scrapy.Field()
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OneB(scrapy.Item):
    # define the fields for your item here like:
    product_code = scrapy.Field()
    product_title_info = scrapy.Field()
    designer_name = scrapy.Field()
    designer_id = scrapy.Field()
    price_info = scrapy.Field()
    #currency = scrapy.Field()
    #file_urls = scrapy.Field()
    #files = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    alter_style_pid = scrapy.Field()
    country = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    houseTitle = scrapy.Field()
    houseName = scrapy.Field()
    houseCity = scrapy.Field()
    houseCityURL = scrapy.Field()
    housePublishedTime = scrapy.Field()
    housePrice = scrapy.Field()
    houseHistoryPrice = scrapy.Field()
    houseArea = scrapy.Field()
    houseAddress = scrapy.Field()
    houseLongitude = scrapy.Field()
    houseLatitude = scrapy.Field()
    houseBaiduLongitude = scrapy.Field()
    houseBaiduLatitude = scrapy.Field()
    pass

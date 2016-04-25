#!/usr/bin/env python
# coding=utf-8

import scrapy
from SpiderLianjia.items import SpiderlianjiaItem

class CityLianjia(scrapy.Spider):
    name = 'CityLianjia'
    allowed_domains = ['lianjia.com']
    start_urls = ['http://cs.lianjia.com/']

    def parse(self, response):
        city_info_query = '//body/div/div/div[@class="city-change animated"]/ul/li'
        for info in response.xpath(city_info_query):
            item = SpiderlianjiaItem()
            item['houseCityURL'] = info.xpath('a/attribute::href').extract()[0]
            item['houseCity'] = info.xpath('a/text()').extract()[0]
            
            yield item


#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson

from Spider5i5j.items import Spider5I5JItem
from Spider5i5j.spiders.startURL import startURL

class city5i5j(scrapy.Spider):
    name = 'city5i5j'
    allowed_domains = ['5i5j.com']
    start_urls = ['http://cs.5i5j.com/exchange']

    def parse(self, response):
        city_page_query = '//body/nav/div/div/ul[@class="city-more-r"]/li/a'
        for info in response.xpath(city_page_query):
            item = Spider5I5JItem()
            item['houseCity'] = info.xpath('text()').extract()[0]
            item['houseCityURL'] = info.xpath('attribute::href').extract()[0]
            yield item

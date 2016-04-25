#!/usr/bin/env python
# coding=utf-8

import scrapy
from SpiderGanji.items import SpiderganjiItem

class cityGanji(scrapy.Spider):
    name = 'cityGanji' 
    allowed_domains = ['ganji.com']
    start_urls = ['http://www.ganji.com/index.htm']

    def parse(self, response):
        item = SpiderganjiItem()
        house_page_query = '//body/div/div[@class="all-city"]/dl/dd/a'
        for info in response.xpath(house_page_query):
            item = SpiderganjiItem()
            item['houseCity'] = info.xpath('text()').extract()[0]
            item['houseCityURL'] = info.xpath('attribute::href').extract()[0]
            yield item


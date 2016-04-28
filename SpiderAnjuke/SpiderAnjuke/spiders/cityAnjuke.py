#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson
from SpiderAnjuke.items import SpideranjukeItem
#from SpiderLianjia.spiders.startURL import startURL

class cityAnjuke(scrapy.Spider):
    name = 'cityAnjuke'
    allowed_domains = ['anjuke.com']
    start_urls = ['http://www.anjuke.com/sy-city.html']

    def parse(self, response):
        house_page_query = '//body/div/div/div[@class="cities_boxer"]/div/dl/dd/a'
        
        for info in response.xpath(house_page_query): 
            item = SpideranjukeItem()
            item['houseCity'] = info.xpath('text()').extract()[0]
            item['houseCityURL'] = info.xpath('attribute::href').extract()[0]
            
            yield item


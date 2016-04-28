#!/usr/bin/env python
# coding=utf-8

import scrapy
from Spider5i5j.items import Spider5I5JItem
from Spider5i5j.spiders.startURL import startURL

class xinfang5i5j(scrapy.Spider):
    name = 'xinfang5i5j'
    allowed_domains = ['5i5j.com']
    start_urls = startURL.xinfangURL

    def parse(self, response):
        #这个XPath可以匹配每个小区并包含经纬度
        house_info_query = '//body/section/div/div/div/ul[@class="list-body"]/li'
        for info in response.xpath(house_info_query):
            item = Spider5I5JItem()
            item['houseCity'] = response.xpath('//body/nav/div/a/span/text()').extract()[0]
            item['houseBaiduLongitude'] = info.xpath('attribute::x').extract()[0]
            item['houseBaiduLatitude'] = info.xpath('attribute::y').extract()[0]
            item['houseName'] = info.xpath('div/h2/a/text()').extract()[0]
            item['housePrice'] = info.xpath('div/dl/dt/h3/text()').extract()[0]
            yield item

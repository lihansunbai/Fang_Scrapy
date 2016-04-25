#!/usr/bin/env python
# coding=utf-8

#引入scrapy库
import scrapy
#引入自己定义的item
from Spider58.items import Spider58Item

class city58(scrapy.Spider):
    name = 'city58'
    allowed_domains = ['cs.58.com/']
    start_urls = ['http://www.58.com/changecity.aspx']


    def parse(self,response):
        city_query = '//body/div/dl[@id="clist"]/dd/a'

        for info in response.xpath(city_query):
            item = Spider58Item()
            item['houseCityURL'] = info.xpath('attribute::href').extract()[0]
            item['houseCity'] =  info.xpath('text()').extract()[0]

            yield item


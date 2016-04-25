#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson
from SpiderGanji.items import SpiderganjiItem
from SpiderGanji.spiders.startURL import startURL

class ershoufangGanji(scrapy.Spider):
    name = 'ershoufangGanji' 
    allowed_domains = ['ganji.com']
    start_urls = startURL.ershoufangURL

    def parse(self, response):
        house_page_query = '//body/div/div/div/ul/li/div/div/a[@class="list-info-title js-title"]'
        for info in response.xpath(house_page_query):
            house_page_href = info.xpath('attribute::href').extract()[0]
            house_page_url = 'http://cs.ganji.com' + house_page_href
            house_page_log = info.xpath('attribute::gjalog_fang').extract()[0]
            temp_time = house_page_log.split('@')[2]
            housePublishedTiem = temp_time.split('=')[1]
            yield scrapy.Request(house_page_url,callback=self.parse_house_page,meta={"time":housePublishedTiem})

    def parse_house_page(self,response):
        item = SpiderganjiItem()
        item['housePublishedTime'] = response.request.meta['time']
        item['houseTitle'] = response.xpath('//html/head/title/text()').extract()[0]
        item['houseCity'] = item['houseCity'] = response.xpath('//head/meta[@name="location"]/attribute::content').extract()[0].split(';')[1].split('=')[1]

        #此XPath节点可以获得房屋的所有基本信息
        house_info_query = '//body/div/div/div/div/div/div/ul[@class="basic-info-ul"]'

        price_query = 'li/b[@class="basic-info-price"]/text()'
        item['housePrice'] = response.xpath(house_info_query).xpath(price_query).extract()[0]

        area_query = 'li[3]/text()'
        temp_area = response.xpath(house_info_query).xpath(area_query).extract()[0]
        item['houseArea'] = temp_area.split('-')[1]

        name_query = 'li[6]/a/text()'
        name_query_2 = 'li[6]/span[2]/text()'
        if response.xpath(house_info_query).xpath(name_query).extract_first() is None:
            item['houseName'] = response.xpath(house_info_query).xpath(name_query_2).extract()[0]
        else:
            item['houseName'] = response.xpath(house_info_query).xpath(name_query).extract()[0]

        district_query = 'li[7]/a/text()'
        temp_district = response.xpath(house_info_query).xpath(district_query).extract()
        houseDistrict = ''
        for dist in temp_district:
            houseDistrict = houseDistrict + '-' + dist
        item['houseDistrict'] = houseDistrict

        address_query = 'li[8]/span[@title]/text()'
        item['houseAddress'] = response.xpath(house_info_query).xpath(address_query).extract()[0]

        #此XPath节点匹配经纬度信息
        position_query = '//body/div/div/div/div/div/div[@id="map_load"]'
        house_position = response.xpath(position_query)
        house_position_1 = house_position.xpath('attribute::data-ref').extract()[0]
        house_position_json = demjson.decode(house_position_1)
        house_position_split = house_position_json['lnglat'].split(',')

        item['houseBaiduLongitude'] = house_position_split[0][1:-1]
        item['houseBaiduLatitude'] = house_position_split[1]


        yield item
        

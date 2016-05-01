#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson
from SpiderAnjuke.items import SpideranjukeItem
from SpiderAnjuke.spiders.startURL import startURL

class xinfangAnjuke(scrapy.Spider):
    name = 'xinfangAnjuke'
    allowed_domains = ['anjuke.com']
    start_urls = startURL.xinfangURL

    def parse(self, response):
        house_page_query = '//body/div/div/div/div[@class="key-list"]/div' 
        for info in response.xpath(house_page_query): 
            house_page_url = info.xpath('attribute::data-link').extract()[0]
            
            yield scrapy.Request(house_page_url,callback=self.parse_house_page)

    def parse_house_page(self,response):
        item = SpideranjukeItem()
        item['houseTitle'] = response.xpath('//html/head/title/text()').extract()[0]
        item['houseName'] = response.xpath('//body/div/div/div/div[@class="lp-tit"]/h1/text()').extract()[0]

        #这个网页可以通过正则表达匹配出非常多的原始信息
        origin_info_1 = response.xpath('//body/script[@type="text/javascript"]/text()').re(r'XF\.Vars\.groupsojData.*\{.*\}')[0] 

        if origin_info_1 is None:
            pass
        else:
            house_info_json = demjson.decode(origin_info_1[22:])
            item['houseCity'] = house_info_json['p']['data']['city_name']
            item['houseAddress'] = house_info_json['p']['data']['loupan_info']['basic']['address']
            item['houseLatitude'] = house_info_json['p']['data']['loupan_info']['map']['lat']
            item['houseLongitude'] = house_info_json['p']['data']['loupan_info']['map']['lng']
            item['houseBaiduLongitude'] = house_info_json['p']['data']['loupan_info']['map']['baidu_lng']
            item['houseBaiduLatitude'] = house_info_json['p']['data']['loupan_info']['map']['baidu_lat']

            houseHistoryPrice_list = house_info_json['p']['data']['price_mothly_list']
            item['houseHistoryPrice'] = {}
            for i in houseHistoryPrice_list:
                date = i['date_index']
                item['houseHistoryPrice'][date] = i['price'] 

        yield item 

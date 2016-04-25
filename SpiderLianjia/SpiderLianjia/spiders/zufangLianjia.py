#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson
from SpiderLianjia.items import SpiderlianjiaItem
from SpiderLianjia.spiders.startURL import startURL

class zufangLianjia(scrapy.Spider):
    name = 'zufangLianjia'
    allowed_domains = ['lianjia.com']
    start_urls = startURL.zufangURL

    def parse(self, response):
        house_page_query = '//body/div/div/div/div/ul[@id="house-lst"]/li/div[@class="info-panel"]/h2/a[@href]'
        for info in response.xpath(house_page_query):
            house_page_href = info.xpath('attribute::href').extract()[0]
            house_page_url =  house_page_href
            
            yield scrapy.Request(house_page_url,callback=self.parse_house_page,dont_filter=True)

    def parse_house_page(self,response):
        item = SpiderlianjiaItem()
        item['houseTitle'] = response.xpath('//html/head/title/text()').extract()[0]
        item['houseCity'] = response.xpath('//head/script/text()').re(r'city_name.*\'')[0].split('\'')[-2]

        #这个网页只能通过正则表达式匹配信息
        item['houseName'] = response.xpath('//html').re(r'resblockName.*,')[0].split('\'')[1]
        item['housePrice'] = response.xpath('//html').re(r'totalPrice.*,')[0].split('\'')[1]
        item['houseArea'] = response.xpath('//html').re(r'area.*,')[0].split('\'')[1]
        item['houseBaiduLongitude'] = response.xpath('//html').re(r'resblockPosition.*,')[0].split('\'')[1].split(',')[1]
        item['houseBaiduLatitude'] = response.xpath('//html').re(r'resblockPosition.*,')[0].split('\'')[1].split(',')[0]

        #构造新的数据请求历史价格数据
        hid = response.xpath('//html').re(r'houseId.*,')[0].split('\'')[1]
        rid = response.xpath('//html').re(r'resblockId.*,')[0].split('\'')[1]
        history_price_query = 'http://cs.lianjia.com/ershoufang/housestat?hid='+ hid +'&rid=' + rid
        yield scrapy.Request(history_price_query,callback=self.parse_history_price_page,meta={'house_item':item},dont_filter=True)

    def parse_history_price_page(self, response):
        item = response.request.meta['house_item']
        response_json = demjson.decode(response.body)
        item['houseHistoryPrice'] = {
            'time' : response_json['data']['trend']['resblockTrend']['month'],
            'price' : response_json['data']['trend']['resblockTrend']['price']['total']
        }

        item['housePublishedTime'] = response_json['data']['trend']['resblockTrend']['month'][0]

        yield item 

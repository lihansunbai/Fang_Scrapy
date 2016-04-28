#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson
from SpiderAnjuke.items import SpideranjukeItem
from SpiderAnjuke.spiders.startURL import startURL

class ershoufangAnjuke(scrapy.Spider):
    name = 'ershoufangAnjuke'
    allowed_domains = ['anjuke.com']
    start_urls = startURL.ershoufangURL

    def parse(self, response):
        house_page_query = '//body/div/div/div/ul[@id="house-list"]/li'
        for info in response.xpath(house_page_query): 
            page_url_query = 'div/div[@class="house-title"]/a/attribute::href'
            house_page_url = info.xpath(page_url_query).extract()[0]
            
            yield scrapy.Request(house_page_url,callback=self.parse_house_page)

    def parse_house_page(self,response):
        item = SpideranjukeItem()
        item['houseTitle'] = response.xpath('//html/head/title/text()').extract()[0]
        item['houseCity'] = response.xpath('//body/div/div/div/div/div/div/span[@class="city"]/text()').extract()[0]
        item['houseName'] = response.xpath('//body/div/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="litem fl"]/dl[5]/dd/a/text()').extract()[0]
        item['houseAddress'] = response.xpath('//body/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="litem fl"]/dl[3]/dd/text()').extract()[0]
        item['housePrice'] = response.xpath('//body/div/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="litem fl"]/dl[1]/dd/strong/span/text()').extract()[0]
        item['houseArea'] = response.xpath('//body/div/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="ritem fr"]/dl[2]/dd/text()').extract()[0]
        #这里看开始通过正则表达匹配经纬度
        lonlat = response.xpath('/html').re(r'\&lat.*\&')[0]
        if lonlat:
            item['houseBaiduLatitude'] = lonlat.split('&')[1].split('=')[1]
            item['houseBaiduLongitude'] = lonlat.split('&')[2].split('=')[1]
            #这里还要在匹配一个comid用于获取历史价格数据
            house_comid =  lonlat.split('&')[3].split('=')[1]

        else:
            item['houseBaiduLatitude'] = ''
            item['houseBaiduLongitude'] = ''
            
        #如果可以匹配到comid在进行历史价格查询
        if house_comid:
            house_price_url = 'http://cs.anjuke.com/v3/ajax/prop/pricetrend/?commid=' + house_comid
            yield scrapy.Request(house_price_url,callback=self.parse_house_price,meta={'items':item})
        else:
            yield item

    def parse_house_price(self,response):
        item = response.request.meta['items']
        response_json = demjson.decode(response.body)
        item['houseHistoryPrice'] = response_json['community']
        yield item

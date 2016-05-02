#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson
import time
from SpiderLianjia.items import SpiderlianjiaItem
from SpiderLianjia.spiders.startURL import startURL

class ershoufangLianjia(scrapy.Spider):
    name = 'ershoufangLianjia'
    allowed_domains = ['lianjia.com']
    start_urls = startURL.ershoufangURL

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

        info_parse_1 = response.xpath('//html').re(r'resblockName.*,')
        if info_parse_1:
            yield scrapy.Request(response.request.url,callback=self.parse_house_page_res,dont_filter=True,meta={'items':item})
        else:
            yield scrapy.Request(response.request.url,callback=self.parse_house_page_com,dont_filter=True,meta={'items':item})


    def parse_house_page_res(self,response):
        item = response.request.meta['items']
        #这个类型的网页只能通过正则表达式匹配信息
        item['houseName'] = response.xpath('//html').re(r'resblockName.*,')[0].split('\'')[1]
        item['housePrice'] = response.xpath('//html').re(r'totalPrice.*,')[0].split('\'')[1]
        item['houseArea'] = response.xpath('//html').re(r'area.*,')[0].split('\'')[1]
        if response.xpath('//html').re(r'resblockPosition.*,'):
            item['houseBaiduLongitude'] = response.xpath('//html').re(r'resblockPosition.*,')[0].split('\'')[1].split(',')[1]
            item['houseBaiduLatitude'] = response.xpath('//html').re(r'resblockPosition.*,')[0].split('\'')[1].split(',')[0]
        else:
            item['houseBaiduLongitude'] = ''
            item['houseBaiduLatitude'] = ''


        #构造新的数据请求历史价格数据
        if response.xpath('//html').re(r'houseId.*,'):
            hid = response.xpath('//html').re(r'houseId.*,')[0].split('\'')[1]
            rid = response.xpath('//html').re(r'resblockId.*,')[0].split('\'')[1]
            url_tmp = response.request.url.split('/')[2]
            history_price_query = 'http://' + url_tmp + '/ershoufang/housestat?hid='+ hid +'&rid=' + rid
            
            yield scrapy.Request(history_price_query,callback=self.parse_history_price_page_res,meta={'house_item':item},dont_filter=True)
        else:
            #获得发布时间的月份
            time_list = time.localtime()
            if time_list[1] < 10:
                times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
            else:
                times = '%d'%time_list[0]+'%d'%time_list[1]

            item['houseHistoryPrice'] = {
                'time' : [times,],
                'price' : [item['housePrice'],]
            }
            yield item


    def parse_house_page_com(self,response):
        item = response.request.meta['items']
        house_price_query = '//body/div/section/div/div[@class="desc-text clear"]/dl/dd/span/strong[@class="ft-num"]/text()'
        item['housePrice'] = response.xpath(house_price_query).extract()[0]

        house_area_query = '//body/div/section/div/div[@class="desc-text clear"]/dl/dd/span/i/text()'
        item['houseArea'] = response.xpath(house_area_query).extract()[0].replace('/','').strip()[:-1]

        house_name_query = '//body/div/section/div/div[@class="desc-text clear"]/dl/dd/a[@data-el="community"]/text()'
        if response.xpath(house_name_query).extract():
            item['houseName'] = response.xpath(house_name_query).extract()[0]
        else:
            house_name_query = '//body/div/section/div/div[@class="desc-text clear"]/dl[@class="clear"]/dd/text()'
            item['houseName'] = response.xpath(house_name_query).extract()[0]

        #这里匹配经纬度
        lnglat_query = response.xpath('/html').re(r'coordinates.*?]')
        if lnglat_query:
            item['houseBaiduLatitude'] = lnglat_query[0].split('[')[-1].split(',')[0]
            item['houseBaiduLongitude'] = lnglat_query[0].split('[')[-1].split(',')[1][:-1]
        else:
            item['houseBaiduLatitude'] = ''
            item['houseBaiduLongitude'] = ''

        #这里匹配communityCode
        communityCode_query = response.xpath('/html').re(r'\?communityCode=\d*')
        if communityCode_query:
            url_tmp = response.request.url.split('/')[2]
            history_price_query = 'http://' + url_tmp + '/api/getcommunityhistory' + communityCode_query[0]
            yield scrapy.Request(history_price_query,callback=self.parse_history_price_page_com,meta={'house_item':item},dont_filter=True)
        else:
            #获得发布时间的月份
            time_list = time.localtime()
            if time_list[1] < 10:
                times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
            else:
                times = '%d'%time_list[0]+'%d'%time_list[1]

            item['houseHistoryPrice'] = {
                'time' : [times,],
                'price' : [item['housePrice'],]
            }
            yield item


    def parse_history_price_page_res(self, response):
        item = response.request.meta['house_item']
        response_json = demjson.decode(response.body)
        item['houseHistoryPrice'] = {
            'time' : response_json['data']['trend']['resblockTrend']['month'],
            'price' : response_json['data']['trend']['resblockTrend']['price']['total']
        }

        yield item 

    def parse_history_price_page_com(self,response):
        item = response.request.meta['house_item']
        response_json = demjson.decode(response.body)
        item['houseHistoryPrice'] = {
            'time' : response_json['trends']['name'],
            'price' : response_json['trends']['price']
        }

        yield item 

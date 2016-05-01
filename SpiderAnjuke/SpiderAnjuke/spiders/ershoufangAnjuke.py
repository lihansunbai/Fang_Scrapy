#!/usr/bin/env python
# coding=utf-8

import scrapy
import demjson
import time
import string
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
        #匹配房屋地址
        house_address_query = '//body/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="litem fl"]/dl[3]/dd/text()'
        house_address = response.xpath(house_address_query).extract()
        if house_address:
            item['houseAddress'] = response.xpath(house_address_query).extract()[0]
        else:
            item['houseAddress'] = 'N/A'

        item['housePrice'] = response.xpath('//body/div/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="litem fl"]/dl[1]/dd/strong/span/text()').extract()[0]
        item['houseArea'] = response.xpath('//body/div/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="ritem fr"]/dl[2]/dd/text()').extract()[0]
        house_area = string.atof(item['houseArea'][:-2])
        #匹配房屋小区名称
        house_name_query_1 = '//body/div/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="litem fl"]/dl[5]/dd/a/text()'
        house_name_query_2 = '//body/div/div/div/div/div/div/div/div/div[@class="phraseobox cf"]/div[@class="litem fl"]/dl[5]/dd/text()'
        house_name_query = response.xpath(house_name_query_1).extract()
        if house_name_query: 
            item['houseName'] = response.xpath(house_name_query_1).extract()[0].replace('\n','').replace('\t','').replace('\r','').replace(' ','')
        else:
            item['houseName'] = response.xpath(house_name_query_2).extract()[0].replace('\n','').replace('\t','').replace('\r','').replace(' ','')

        #这里看开始通过正则表达匹配经纬度
        lat = response.xpath('/html').re(r'lat=.*?&')
        lng = response.xpath('/html').re(r'lng=.*?&')
        if lat:
            item['houseBaiduLatitude'] = lat[0].split('=')[-1][:-1]
            item['houseBaiduLongitude'] = lng[0].split('=')[-1][:-1]

        else:
            item['houseBaiduLatitude'] = ''
            item['houseBaiduLongitude'] = ''
            
        #如果可以匹配到comid在进行历史价格查询
        house_comid = response.xpath('/html').re(r'comid=.*?&')
        if house_comid:
            comid =  house_comid[0].split('=')[-1][:-1]
            url_1 = response.request.url.split('/')[2]
            house_price_url = 'http://'+ url_1 + '/v3/ajax/prop/pricetrend/?commid=' + comid
            yield scrapy.Request(house_price_url,callback=self.parse_house_price,meta={'items':item})
        else:
            #取得当前时间
            time_list = time.localtime()
            if time_list[1] < 10:
                times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
            else:
                times = '%d'%time_list[0]+'%d'%time_list[1]

            #构造历史数据
            price = (string.atof(item['housePrice'])*10000) / house_area
            item['houseHistoryPrice']= [{times:price}]

            yield item

    def parse_house_price(self,response):
        item = response.request.meta['items']
        house_area = string.atof(item['houseArea'][:-2])
        #就算取得小区ID成功也有可能存在json解析不成功的例子，所以需要再做判断
        #这里解析json的时候需要带返回错误信息，否则返回会报错
        response_json = demjson.decode(response.body,return_errors=True)

        #注意！！！
        #这里判读是否解析成功历史价格数据要判断demjson的返回值是否是list对象
        #具体原因请参看demjson的官方文档
        #if type(response_json[0]) is not type(list()):
        if response_json[1]:
            #取得当前时间
            time_list = time.localtime()
            if time_list[1] < 10:
                times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
            else:
                times = '%d'%time_list[0]+'%d'%time_list[1]

            #构造历史数据
            price = (string.atof(item['housePrice'])*10000) / house_area
            item['houseHistoryPrice']= [{times:price}]
        else:
            #直接从返回数据中取得历史价格数据
            item['houseHistoryPrice'] = response_json[0]['community']

        yield item


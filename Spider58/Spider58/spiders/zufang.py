#!/usr/bin/env python
# coding=utf-8

#引入scrapy库
import scrapy
#引入DEMJOSN库
import demjson

#引入自己定义的item
from Spider58.items import Spider58Item
#引入起始url的位置
from Spider58.spiders.startURL import startURL

class zufang58(scrapy.Spider):
    name = 'zufang58'
    allowed_domains = ['cs.58.com/']
    start_urls = startURL.zufangURL

    def parse(self,response):
        house_page_query = '//body/div/div/div/table/tr/td/a'
        for info in response.xpath(house_page_query):
            house_href = info.xpath('attribute::href').extract()[0]
            house_url = house_href.split('?')[0]
            
            #把发布时间sortid的信息提取进housePublishedTime
            query_1 = 'ancestor::*/ancestor::*/attribute::sortid'
            housePublishedTime = info.xpath(query_1).extract()[0]

            yield scrapy.Request(house_url, callback=self.parse_house_page,meta = {'time':housePublishedTime}, dont_filter=True)

    def parse_house_page(self,response):
        item = Spider58Item()

        item['housePublishedTime'] = response.request.meta['time']
        item['houseTitle'] = response.xpath('//head/title/text()').extract()
        #这里匹配城市信息
        city_query_1 = response.xpath('//head/meta[@name="location"]/attribute::content').extract()
        if city_query_1:
            item['houseCity'] = city_query_1[0].split(';')[1].split('=')[1]
        else:
            city_query_2 = response.xpath('//html').re(r'locallist\:\[.*?\]')[0] 
            city_query_2_json = demjson.decode(city_query_2[10:])
            item['houseCity'] = city_query_2_json[0]['name']
        
        #info_1匹配name,lon,lat,baidulon,baidulat
        info_1 = response.xpath('//html').re(r'\{name\:.*?\'\}')[0]
        info_1_josn = demjson.decode(info_1)
        item['houseName'] = info_1_josn['name']
        item['houseLatitude'] = info_1_josn['lat']
        item['houseLongitude'] = info_1_josn['lon']
        item['houseBaiduLatitude'] = info_1_josn['baidulat']
        item['houseBaiduLongitude'] = info_1_josn['baidulon']

        #info_2匹配面积
        info_2 = response.xpath('//html').re(r'\{\"I\"\:1025.*?\}')[0]
        info_2_josn = demjson.decode(info_2)
        info_2_area = info_2_josn['V']
        item['houseArea'] = info_2_area

        #info_3匹配价格
        info_3 = response.xpath('//html/head').re(r'\{\"I\"\:1016.*?\}')[0]
        info_3_josn = demjson.decode(info_3)
        info_3_price = info_3_josn['V']
        item['housePrice'] = info_3_price 

        #info_4匹配地址
        info_4 = response.xpath('//body/div/div/div/ul[@class="house-primary-content"]/li/div/a/text()').extract()
        temp_addr = ''
        for address in info_4:
            temp_addr = temp_addr + '-' + address
        item['houseAddress'] = temp_addr

        yield item

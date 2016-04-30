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

class ershoufang58(scrapy.Spider):
    name = 'ershoufang58'
    allowed_domains = ['58.com/']
    start_urls = startURL.ershoufangURL


    def parse(self,response):
        for infoid in response.xpath('//body/div/div/div/table/tr/td/p/a').re(r'infoid\=\"\d*'):
            house_page_id = infoid.split('\"')[1]
            #TODO
            #把发布时间sortid的信息提取进housePublishedTime
            query_1 = '//body/div/div/div/table/tr/td/p/a[@infoid="'+ house_page_id +'"]/ancestor::*/ancestor::*/attribute::sortid'
            housePublishedTime = response.xpath(query_1).extract()[0]

            #这里使用split分开提取XPath出来的信息
            #第二部分为房屋信息页面ID 
            #house_page_id = infoid.split('\"')[1]
            house_page_root = response.request.url.split('/')[2]
            house_url = 'http://'+house_page_root+'/ershoufang/' + house_page_id + 'x.shtml'
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
        info_1 = response.xpath('//html').re(r'xiaoqu\:\{name\:.*?\'\}')[0]
        info_1_cut = info_1[7:]
        info_1_josn = demjson.decode(info_1_cut)
        item['houseName'] = info_1_josn['name']
        item['houseLatitude'] = info_1_josn['lat']
        item['houseLongitude'] = info_1_josn['lon']
        item['houseBaiduLatitude'] = info_1_josn['baidulat']
        item['houseBaiduLongitude'] = info_1_josn['baidulon']
        #info_2匹配面积,价格
        info_2 = response.xpath('//html').re(r'\{\"I\"\:1081.*?\}')[0]
        info_2_josn = demjson.decode(info_2)
        info_2_split = info_2_josn['V']
        item['houseArea'] = info_2_split
        info_2 = response.xpath('//html').re(r'\{\"I\"\:1078.*?\}')[0]
        info_2_josn = demjson.decode(info_2)
        info_2_split = info_2_josn['V']
        item['housePrice'] = info_2_split
        #info_3匹配地址
        info_3 = response.xpath('//body/div/section/div/div/div/ul/li/text()').re(r'\<a\s*href.*a\>')
        temp_addr = ''
        for address in info_3:
            temp_addr = temp_addr + '-' + address

        item['houseAddress'] = temp_addr.lstrip('-')

        yield item

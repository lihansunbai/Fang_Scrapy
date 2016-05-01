# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import sys
import string

class SpideranjukePipeline(object):
    def process_item(self, item, spider):
        return item

class xinfangAnjukePipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        #判断是否为安居客新房爬虫
        if spider.name != 'xinfangAnjuke':
            return item

        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果houseHistroyPrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('houseHistoryPrice'):
            return item

        #打开写入的文件和CSV写入模块
        self.file = open('xinfangAnjuke.csv','ab')
        csvWriter = csv.writer(self.file)

        #字典化历史价格
        price_list = dict(item['houseHistoryPrice'])
        
        #格式化item为CSV格式数据
        for house in price_list:
            price_chengjiao = price_list[house]
            price_guapai = price_list[house]
            line = (house,item['houseName'],item['houseCity'],price_chengjiao,price_guapai,item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'])
            csvWriter.writerow(line)

        return item

class ershoufangAnjukePipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        #判断是否为安居客新房爬虫
        if spider.name != 'ershoufangAnjuke':
            return item

        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果houseHistroyPrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('houseHistoryPrice'):
            return item

        #打开写入的文件和CSV写入模块
        self.file = open('ershoufangAnjuke.csv','ab')
        csvWriter = csv.writer(self.file)

        #list化历史价格
        price_list = list(item['houseHistoryPrice'])
        
        #格式化item为CSV格式数据
        for info in price_list:
	    house_area = string.atof(item['houseArea'][:-2])
	    times = info.keys()[0]
	    
            price_chengjiao_tmp = string.atof(info.values()[0])
            price_guapai = string.atof(item['housePrice'])
            price_chengjiao =  price_chengjiao_tmp * house_area / 10000
            
            
            house_address = item['houseAddress'].strip()
            line = (times,item['houseName'],item['houseCity'],price_chengjiao,price_guapai,house_area,house_address,item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'])
            csvWriter.writerow(line)

        return item

class cityAnjukePipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        #判断是否为安居客城市列表爬虫
        if spider.name != 'cityAnjuke':
            return item

        #打开写入的文件
        self.file = open('city.txt','ab')
        
        i = 1
        while i < 51:
            i_str = '%d'%i
            line_1 = '      \''+item['houseCityURL'].encode('utf-8') + '/sale/p' + i_str + '/#filtersort\','
            line_2 = '      \''+item['houseCityURL'].encode('utf-8') + '/loupan/s?p=' + i_str + '\','

            print >> self.file , line_1
            print >> self.file , line_2
            i += 1
        
        return item

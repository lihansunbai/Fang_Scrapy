# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import sys
import time
import string

class Spider5I5JPipeline(object):
    def process_item(self, item, spider):
        return item

class xinfang5i5jPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        #判断是否为我爱我家新房爬虫
        if spider.name != 'xinfang5i5j':
            return item

        #打开写入的文件和CSV写入模块
	self.file = open('xinfang5i5j.csv','ab')
        csvWriter = csv.writer(self.file)

        #取得当前时间
        time_list = time.localtime()
        if time_list[1] < 10:
          times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
        else:
	  times = '%d'%time_list[0]+'%d'%time_list[1]
        
        #格式化item为CSV格式数据
        line = (times,item['houseName'],item['houseCity'],item['housePrice'],item['housePrice'],'N/A',item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseName'])
        csvWriter.writerow(line)
        
        return item


class ershoufang5i5jPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'ershoufang5i5j':
          return item

        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果housePrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('housePrice'):
            return item

        #打开写入的文件和CSV写入模块
	self.file = open('ershoufang5i5j.csv','ab')
        csvWriter = csv.writer(self.file)

        #格式化item为CSV格式数据
        for house in item['housePrice']:
            house_area = item['houseArea'][:-2]
            price_chengjiao_tmp = item['housePrice'][house]['price_chengjiao']
            price_guapai_tmp = item['housePrice'][house]['price_guapai']
            price_chengjiao = string.atof(price_chengjiao_tmp) * string.atof(house_area)
            price_guapai = string.atof(price_guapai_tmp) * string.atof(house_area)
            house_name = item['houseName'].strip()

            line = (house,house_name,item['houseCity'],price_chengjiao,price_guapai,house_area,item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'])
            csvWriter.writerow(line)

        return item


class zufang5i5jPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'zufang5i5j':
          return item

        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果housePrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('housePrice'):
            return item
	  
        #打开写入的文件和CSV写入模块
        self.file = open('zufang5i5j.csv','ab')
        csvWriter = csv.writer(self.file)
        
        #取得当前时间
        time_list = time.localtime()
        if time_list[1] < 10:
          times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
        else:
	    times = '%d'%time_list[0]+'%d'%time_list[1]
	  
        #格式化item为CSV格式数据
        price_chengjiao = item['housePrice']
        price_guapai = item['housePrice']
        house_area_tmp = item['houseArea'].strip()
        house_area = house_area_tmp[:-2]
        house_name = item['houseName'].strip()
        line = (times,house_name,item['houseCity'],price_chengjiao,price_guapai,house_area,item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'])
        csvWriter.writerow(line)
            
        return item

class city5i5jPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'city5i5j':
            return item

        self.file = open('startURL_quanguo.txt','ab')

        i = 1
        while i < 84:
            i_str = '%d'%i
            line_1 = '      \''+item['houseCityURL'].encode('utf-8') + '/exchange/n' + i_str + '/\','
            line_2 = '      \''+item['houseCityURL'].encode('utf-8') + '/community/n' + i_str + '/\','
            line_3 = '      \''+item['houseCityURL'].encode('utf-8') + '/rent/n' + i_str + '/\','

            print >> self.file , line_1
            print >> self.file , line_2
            print >> self.file , line_3
            i += 1
            
        return item

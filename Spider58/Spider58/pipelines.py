# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import sys
import time
import csv
import string

class Spider58Pipeline(object):
    def process_item(self, item, spider):
        return item

class ershoufang58Pipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'ershoufang58':
            return item
        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果housePrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('housePrice'):
            return item

        #打开写入的文件和CSV写入模块
	self.file = open('ershoufang58.csv','ab')
        csvWriter = csv.writer(self.file)
        
        #获得发布时间的月份
        time_tmp = string.atof(item['housePublishedTime'][0:10])
        time_list = time.localtime(time_tmp)
        if time_list[1] < 10:
          times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
        else:
	  times = '%d'%time_list[0]+'%d'%time_list[1]
	  
        #格式化item为CSV格式数据       
        price_chengjiao = item['housePrice']
        price_guapai = item['housePrice']
        line = (times,item['houseName'],item['houseCity'],price_chengjiao,price_guapai,item['houseArea'],item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'][0].strip())
        csvWriter.writerow(line)


        return item

class zufang58Pipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'zufang58':
            return item
	  
        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果housePrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('housePrice'):
            return item

        #打开写入的文件和CSV写入模块
	self.file = open('zufang58.csv','ab')
        csvWriter = csv.writer(self.file)
        
        #获得发布时间的月份
        time_tmp = string.atof(item['housePublishedTime'][0:10])
        time_list = time.localtime(time_tmp)
        if time_list[1] < 10:
          times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
        else:
	  times = '%d'%time_list[0]+'%d'%time_list[1]
	  
        #格式化item为CSV格式数据       
        price_chengjiao = item['housePrice']
        price_guapai = item['housePrice']
        line = (times,item['houseName'],item['houseCity'],price_chengjiao,price_guapai,item['houseArea'],item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'][0].strip())
        csvWriter.writerow(line)

        return item
    
class city58Pipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def process_item(self,item,spider):
        if spider.name != 'city58':
            return item

        self.file = open('startURL_quanguo.txt','ab')
        
        i = 1
        while i < 71:
            i_str = '%d'%i
            line_1 = '      \''+item['houseCityURL'].encode('utf-8') + 'ershoufang/pn' + i_str + '/\','
            line_2 = '      \''+item['houseCityURL'].encode('utf-8') + 'zufang/pn' + i_str + '/\','

            print >> self.file , line_1
            print >> self.file , line_2
            i += 1
        return item

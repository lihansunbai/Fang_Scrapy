# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import csv
import time
import string

class SpiderganjiPipeline(object):
    def process_item(self, item, spider):
        return item

class xinfangGanjiPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'xinfangGanji':
            return item

        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果housePrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('housePrice'):
            return item

        #打开写入的文件和CSV写入模块
	self.file = open('xinfangGanji.csv','ab')
        csvWriter = csv.writer(self.file)
        
        #获得发布时间的月份
        time_tmp = string.atof(item['housePublishedTime'][0:10])
        time_list = time.localtime(time_tmp)
        if time_list[1] < 10:
          times = '%d'%time_list[0]+'0'+'%d'%time_list[1]
        else:
	  times = '%d'%time_list[0]+'%d'%time_list[1]
	  
        #格式化item为CSV格式数据       
        house_area = item['houseArea']
        price_chengjiao_tmp = item['housePrice']
        price_guapai_tmp = item['housePrice']
        price_chengjiao = string.atof(price_chengjiao_tmp) / string.atof(house_area) * 10000
        price_guapai = string.atof(price_guapai_tmp) / string.atof(house_area) * 10000
        house_name = item['houseName'].strip()
        line = (times,house_name,item['houseCity'],price_chengjiao,price_guapai,item['houseArea'],item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'])
        csvWriter.writerow(line)


        return item


class ershoufangGanjiPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'ershoufangGanji':
            return item
        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果housePrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('housePrice'):
            return item
        #打开写入的文件和CSV写入模块
	self.file = open('ershoufangfangGanji.csv','ab')
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
        house_name = item['houseName'].strip()
        line = (times,house_name,item['houseCity'],price_chengjiao,price_guapai,item['houseArea'].strip(),item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'])
        csvWriter.writerow(line)

        return item


class zufangGanjiPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'zufangGanji':
            return item

        #判断是否存在历史价格数据
        #这里要用字典类型中的get方法来判断，否则会报错。
        #原因是如果housePrice不存在，那么字典旧无法索引找到此项，返回错误；而使用get方法则返回空。
        if not item.get('housePrice'):
            return item

        #打开写入的文件和CSV写入模块
	self.file = open('zufangfangGanji.csv','ab')
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
        house_name = item['houseName'].strip()
        line = (times,house_name,item['houseCity'],price_chengjiao,price_guapai,item['houseArea'].strip(),item['houseAddress'],item['houseBaiduLatitude'],item['houseBaiduLongitude'],item['houseTitle'])
        csvWriter.writerow(line)
        return item
    
class cityGanjiPipeline(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        
    def process_item(self,item,spider):
        if spider.name != 'cityGanji':
            return item

        self.file = open('startURL_quanguo.txt','ab')
        
        i = 1
        while i < 71:
            i_str = '%d'%i
            line_1 = '      \''+item['houseCityURL'].encode('utf-8') + 'fang12/o' + i_str + '/\','
            line_2 = '      \''+item['houseCityURL'].encode('utf-8') + 'fang5/o' + i_str + '/\','
            line_3 = '      \''+item['houseCityURL'].encode('utf-8') + 'fang1/o' + i_str + '/\','

            print >> self.file , line_1
            print >> self.file , line_2
            print >> self.file , line_3
            i += 1
        return item


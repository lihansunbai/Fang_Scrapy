# Fang_Scrapy
这是一个作者毕业设计的爬虫，爬取58同城、赶集网、链家、安居客、我爱我家网站的房价交易数据。
This is a web Crawl. I write it for a undergraduate study project.

欢迎使用！
恳请上面网站的鹳狸猿不要和谐我，我没有天天开着爬的～～～

#关于AWK文的使用方法
File_catalog.awk提供了一套处理爬虫数据的算法。算法使用GNU工具awk语言实现。
使用awk程序用此算法处理后数据可以按月和房屋类型拆分为不同文件。
使用方法：
Linux/Unix（或者其他可以使用awk程序的平台）
awk -f [File_catalog.awk的位置] [需要处理的爬虫数据（文件名必须包含xinfang/ershoufang/zufang，数据第一列必须为年月的六位数字如201604）]

# License
请勿用于商业用途！
欢迎Fork，欢迎Watch，欢迎Star！

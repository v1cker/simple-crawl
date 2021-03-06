#!/usr/bin/env python
#coding:utf-8
"""
  Author:  fiht --<fiht@qq.com>
  Purpose: 增量式爬取网站
  Created: 2016年06月20日
"""
#import geoip2.database
import scrapy
from fiveUrl.items import FiveurlItem
from fiveUrl.items import UrlInjection
import socket
from urlparse import urlparse
import pymongo
url_set = set()
sqlInjection_set = set()
#ip_database = geoip2.database.Reader('../1.mmdb')
########################################################################
class test(scrapy.spiders.Spider):
    """test Demo"""
    name = 'main'
#    start_urls = ['http://yinyue.kuwo.cn/']
    def __init__(self):
        db = pymongo.MongoClient('119.29.70.15')['edu_cns']['things']
        things = db.find_one({'scrapyed':{'$exists':False}})
        db.update({'_id':things['_id']},{'$set':{'scrapyed':'1'}})
        self.start_urls =[ 'http://%s'%i for i in things['subDomains']]
        self.allowed_domains = [things['host']]
        print things
        self.host = things['host']
        self._id = things['_id']
    #----------------------------------------------------------------------
    def parse(self,response):
        """parse"""
        if not hasattr(response,'xpath'):
            return
        for url in response.xpath('//*[@href]/@href').extract():
            url = response.urljoin(url)  # 转化成绝对路径
            yield scrapy.Request(url)
            #five_urlItem = FiveurlItem()
            #from_url = response.request.headers.get('Referer')
            #five_urlItem['url']=url
            #five_urlItem['source_url']=from_url
            #yield five_urlItem
            if '=' in url and '.css' not in url and 'javascript:' not in url and "tree.TreeTempUrl" not in url and '?' in url:
                item = UrlInjection()
                item['url'] = url
                item['_id'] = self._id
                yield item

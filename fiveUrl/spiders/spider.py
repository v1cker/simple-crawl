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
url_set = set()
sqlInjection_set = set()
#ip_database = geoip2.database.Reader('../1.mmdb')
########################################################################
class Util:
    """工具类"""
    #----------------------------------------------------------------------
    @staticmethod
    #----------------------------------------------------------------------
    def ip_isChina(ip):
        """本地的数据"""
        try:
            result = ip_database.country(socket.gethostbyname(ip)).country.name=='China'
        except Exception:
            return False
        return result
    #----------------------------------------------------------------------
    @staticmethod
    def canCrawl(url):
        """给一个url返回可不可以抓取,依赖全局变量"""
        if 'http' not in url:
            return False
        netloc = urlparse(url)[1]
        if netloc in url_set: #or 'gov.cn' not in netloc:
            return False
        return True #不对ip进行检验
        return Util.ip_isChina(ip)
    #----------------------------------------------------------------------
    @staticmethod
    def add_toInjection(url,netloc=None):
        things = urlparse(url)
        if things[1]+things[2] not in sqlInjection_set:
            sqlInjection_set.add(things[1]+things[2])
            return True
########################################################################
class test(scrapy.spiders.Spider):
    """test Demo"""
    name = 'main'
#    start_urls = ['http://yinyue.kuwo.cn/']
    start_urls = ['http://%s'%i.strip() for i in open('target')]
#    allowed_domains = ['gov.cn']
    #----------------------------------------------------------------------
    def parse(self,response):
        """parse"""
        if not hasattr(response,'xpath'):
            return
        for url in response.xpath('//*[@href]/@href').extract():
            url = response.urljoin(url)  # 转化成绝对路径
            if 'http' in url: #主要是去掉一些奇怪的协议的干扰
                yield scrapy.Request(url)
            five_urlItem = FiveurlItem()
            netloc = urlparse(url)[1]
            from_netloc = response.request.headers.get('Referer')
            five_urlItem['netloc']=netloc
            five_urlItem['from_netloc']=from_netloc
            yield five_urlItem
            if '=' in url and '.css' not in url:
                item = UrlInjection()
                item['url'] = url
                yield item

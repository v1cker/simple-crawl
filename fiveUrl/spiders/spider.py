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
import json
url_set = set()
sqlInjection_set = set()
from get_form import get_sth
#ip_database = geoip2.database.Reader('../1.mmdb')
########################################################################
class test(scrapy.spiders.Spider):
    """test Demo"""
    name = 'main'
#    start_urls = ['http://yinyue.kuwo.cn/']
    start_urls = ['http://%s'%i.strip() for i in open('target')]
#    allowed_domains = ['tsinghua.edu.cn']
    #----------------------------------------------------------------------
    def parse(self,response):
        """parse"""
        if not hasattr(response,'xpath'):
            return
        for url in response.xpath('//*[@href]/@href').extract():
            url = response.urljoin(url)  # 转化成绝对路径
            if 'http' in url[0:5]:  # 主要是去掉一些奇怪的协议的干扰
                yield scrapy.Request(url)
            five_urlItem = FiveurlItem()
            if '=' in url and '.css' not in url: # 找到所有含有等号的url
                item = UrlInjection()
                item['url'] = url
                yield item
        with_post_data = get_sth(response.body)
        data = [response.url,with_post_data]
        with open('post_data','a+') as e:
            e.writelines(response.url)
            e.writelines('---')
            for form in with_post_data:
                e.writelines(str(form))
                e.writelines('  ')
            e.writelines('\n')

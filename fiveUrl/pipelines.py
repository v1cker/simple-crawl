# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from pymongo import MongoClient
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
import sys
from urlparse import urlparse
from scrapy.exceptions import DropItem
from fiveUrl.items import FiveurlItem
from fiveUrl.items import UrlInjection
reload(sys)
sys.setdefaultencoding('utf-8')
########################################################################
class MongoDBPipeline:
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            item['hasScaned']=0
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
#            self.collection.insert({'hasScaned':0})
        return item


class FiveurlPipeline():
    def __init__(self):
        self.inject_hosts = set()
        self.url_host = set()
    #----------------------------------------------------------------------
    # 转化的形式：https://www.baidu.com/s?ie&f=&inputT=&oq=&prefixsug=&rqlang=&rsp=&rsv_bp=&rsv_enter=&rsv_pq=&rsv_sug1=&rsv_sug2=&rsv_sug3=&rsv_sug4=&rsv_sug7=&rsv_t=&tn=&wd
    @staticmethod
    def format_url(url):
        """将链接中带的参数转化成xxx"""
        things = url.split('=')
        for i in range(len(things)):
            if '&' in things[i]:
                things[i] = things[i][things[i].find('&'):]
        return_thing = things[0]+'='+'='.join(sorted(things[1:]))
        return return_thing[0:return_thing.rfind('=')]
    
    def process_item(self, item, spider):
        if type(item)==UrlInjection: #处理sql注入的链接
            key_ = FiveurlPipeline.format_url(item['url'])
            if key_ not in self.inject_hosts:
                self.inject_hosts.add(key_)
                with open('injection','a+') as e:
                    e.writelines(item['url']+'\n')
                return item

        elif type(item)==FiveurlItem: 
            netloc = urlparse(item['url'])[1]
            if netloc not in self.url_host:
                self.url_host.add(netloc)
                with open('FiveUrl', 'a+') as e:
                    if item['source_url']==None:
                        item['source_url']='None'
                    source_netloc = urlparse(item['source_url'])[1]
                    if netloc!=source_netloc:
                        e.writelines(netloc+' '+source_netloc+'\n')
                return item
        else:
            print '-------你妈炸了-------'
            print item,type(item)

if __name__=='__main__':
    print FiveurlPipeline().format_url('https://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&tn=monline_dg&wd=wordpress%20keywords%20description&oq=windows%20KeyWords&rsv_pq=e1a0507200035f31&rsv_t=d8d2eyqKRfSj7pCTzFOZusxJP5YykMb48%2BZjnDxlwRYRY6xgbPFYW1uG6bPtWg%2FKkA&rqlang=cn&rsv_enter=1&inputT=10413&rsv_sug3=54&rsv_sug1=7&rsv_sug7=100&rsv_sug2=0&prefixsug=wordpress%20KeyWords&rsp=0&rsv_sug4=11064')
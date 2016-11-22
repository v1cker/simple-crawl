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
        self.se = set()
    def process_item(self, item, spider):
        valid = True
        url = item['url']
        key = url[:url.find('?')] 
        if key not in self.se:
#            self.collection.insert(dict(item))
#            i.update({'host':'hnjd.edu.c3n'},{'$push':{'url':{"$each":[6]}}})
            self.collection.update({'_id':item['_id']},{"$push":{"url":item['url']}})
            self.se.add(key)
        else:
            pass
        return item


class FiveurlPipeline():
    def __init__(self):
        self.inject_hosts = set()
        self.url_host = set()
    def process_item(self, item, spider):
        if type(item)==UrlInjection: #处理sql链接
            things = urlparse(item['url'])
            key_ = things[1]
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

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
    def process_item(self, item, spider):
        if isinstance(item,UrlInjection): #处理sql链接
            things = urlparse(item['url'])
            if things[1] + things[2] not in self.inject_hosts:
                self.inject_hosts.add(things[1] + things[2])
                with open('injection','a+') as e:
                    e.writelines(item['url']+'\n')
                    e.close()
                return item
            else:
                raise DropItem('过滤掉一个item')

        if isinstance(item,FiveurlItem):
            netloc = urlparse(item['netloc'])[1]
            if netloc not in self.url_host:
                self.url_host.add(netloc)
                with open('FiveUrl', 'a+') as e:
                    if item['from_netloc']==None:
                        item['from_netloc']='None'
                    e.writelines(item['netloc']+' '+urlparse(item['from_netloc'])[1]+'\n')
                    e.close()
                return item
        else:
            print '-------你妈炸了-------'
            print item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from lxml import html

class IsentiaPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline:
    """ The pipeline to save data into MongoDB """
    def __init__(self):
        """ Initialize class and set connection properties

        :return:
        """
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        """ Overriden method to save item

        :param item: Item to be procesed
        :param spider: The spider is being used
        :return: Item has ben processed
        """
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("News added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

class CleanupHTMLPipeline:
    def process_item(self, item, spider):
        """ Overriden method to clean up HTML

        :param item: Item to be procesed
        :param spider: The spider is being used
        :return: Item has ben processed
        """
        if item['content']:
            content = html.document_fromstring(item['content'])
            item['content'] = content.text_content()

        return item
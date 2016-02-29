# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os.path
import logging

from scrapy.conf import settings
from scrapy.exceptions import DropItem

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.mongodbutils import MongoDBUtils


class MongoDBPipeline(object):
    """ The pipeline to save data into MongoDB """

    def __init__(self):
        pass

    def open_spider(self, spider):
        """ Open connection when spider is opened
        :param spider: The spider is opened
        :return:
        """
        connection_string = MongoDBUtils.create_connection_string(
            settings['MONGODB_SERVER'], settings['MONGODB_PORT'],
            settings['MONGODB_USER'], settings['MONGODB_PASSWORD'])
        self.client = MongoDBUtils.connect(connection_string)
        self.collection = MongoDBUtils.get_collection(self.client,
                                                      settings['MONGODB_DB'], settings['MONGODB_COLLECTION'])

    def close_spider(self, spider):
        """ Close connection when spider is closed
        :param spider: The spider is closed
        :return:
        """
        self.client.close()

    def process_item(self, item, spider):
        """ Overriden method to save item

        :param item: Item to be procesed
        :param spider: The spider is being used
        :return: Item has ben processed
        """
        valid = True
        if not item:
            valid = False
            raise DropItem("Missing {0}!".item)

        if valid:
            self.collection.update({'link': item['link']}, dict(item), upsert=True)
            logging.info("News added to MongoDB database!")

        return item


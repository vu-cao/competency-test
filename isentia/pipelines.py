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
        self.__client = None
        self.__collection = None

    def open_spider(self, spider):
        """ Open connection when spider is opened
        :param spider: The spider is opened
        :return:
        """
        connection_string = MongoDBUtils.create_connection_string(
            settings['MONGODB_SERVER'], settings['MONGODB_PORT'],
            settings['MONGODB_USER'], settings['MONGODB_PASSWORD'])
        self.__client = MongoDBUtils.connect(connection_string)
        self.__collection = MongoDBUtils.get_collection(self.__client,
                                                      settings['MONGODB_DB'], settings['MONGODB_COLLECTION'])

    def close_spider(self, spider):
        """ Close connection when spider is closed
        :param spider: The spider is closed
        :return:
        """
        self.__client.close()

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
            # Insert into MongoDB collection
            self.__collection.insert(dict(item))
            logging.info("News added to MongoDB database!")

        return item

    @property
    def collection(self):
        return self.__collection

    @collection.setter
    def collection(self, collection):
        self.__collection = collection

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import os.path

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from lxml import html

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.mongodbutils import MongoDBUtils


class MongoDBPipeline:
    """ The pipeline to save data into MongoDB """
    def __init__(self):
        """ Initialize class and set connection properties

        :return:
        """
        connection_string = MongoDBUtils.create_connection_string(
            settings['MONGODB_SERVER'], settings['MONGODB_PORT'],
            settings['MONGODB_USER'], settings['MONGODB_PASSWORD'])
        self.collection = MongoDBUtils.connect(connection_string,
                                               settings['MONGODB_DB'], settings['MONGODB_COLLECTION'])

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
            self.collection.update({'link': item['link']}, dict(item), upsert=True)
            self.logger.info("News added to MongoDB database!")

        return item


class CleanupHTMLPipeline:
    """ Pipeline class to clean up html tags in item['content'] """

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

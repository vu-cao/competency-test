# -*- coding: utf-8 -*-
import sys
import os.path

import unittest

import mongomock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from isentia.items import NewsItem
from isentia.pipelines import MongoDBPipeline


class MongodbPipelineTest(unittest.TestCase):
    """ Test cases for isentia.pipelines.MongoDBUtils class """

    def setUp(self):
        """ Setup test case
        :return:
        """
        self.collection = mongomock.Connection().db.collection

        # Setup mock data to test
        self.news = NewsItem()
        self.news['domain'] = "www.google.com.au"
        self.news['link'] = "www.google.com.au/calendar"
        self.news['introduction'] = "This is TEST Introduction"
        self.news['headline'] = "This is TEST headline"
        self.news['content'] = "This is TEST content"
        self.news['author'] = "This is TEST author"
        self.news['category'] = "This TEST category"
        self.news['date'] = "This TEST date"

    def test_process_item(self):
        """ Test case for process_item method
        :return:
        """

        pipeline = MongoDBPipeline()
        pipeline.collection = self.collection
        pipeline.process_item(self.news, spider=None)

        cursor = self.collection.find()
        self.assertEqual(cursor.count(), 1, "Should only have 1 document but have %d" % cursor.count())

if __name__ == '__main__':
    unittest.main()
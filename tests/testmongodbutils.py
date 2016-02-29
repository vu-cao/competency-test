# -*- coding: utf-8 -*-
import unittest
import pymongo
import sys
import os.path

import mongomock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from isentia.items import NewsItem
from utils.mongodbutils import MongoDBUtils


class MongodbUtilsTestCase(unittest.TestCase):
    """ Test cases for utils.mongodbutils.MongoDBUtils class """

    def setUp(self):
        """ Setup test case
        :return:
        """
        self.collection = mongomock.Connection().db.collection

        # Setup mock data to test
        news = NewsItem()
        news['domain'] = "www.google.com.au"
        news['link'] = "www.google.com.au/calendar"
        news['introduction'] = "This is TEST Introduction"
        news['headline'] = "This is TEST headline"
        news['content'] = "This is TEST content"
        news['author'] = "This is TEST author"
        news['category'] = "This TEST category"
        news['date'] = "This TEST date"

        news1 = NewsItem()
        news1['domain'] = "www.yahoo.com.au"
        news1['link'] = "www.yahoo.com.au/calendar"
        news1['introduction'] = "This is TEST Introduction 1"
        news1['headline'] = "This is TEST headline 1"
        news1['content'] = "This is TEST content 1"
        news1['author'] = "This is TEST author 1"
        news1['category'] = "This TEST category 1"
        news1['date'] = "This TEST date 1"

        objects = [dict(news), dict(news1)]

        # Insert mock data into mockmongo
        for obj in objects:
            obj['_id'] = self.collection.insert(obj)

    def test_search(self):
        """ Test case for search method
        :return:
        """
        # Test filter feature
        filters = {'domain': "www.google.com.au"}
        sorts = [('date', pymongo.ASCENDING)]

        data = MongoDBUtils.search(self.collection, filters, sorts)
        self.assertEqual(len(data), 1, "Should only have 1 document but have %d" % len(data))

        # Test sort feature
        filters = {}
        sorts = [('date', pymongo.ASCENDING)]

        data = MongoDBUtils.search(self.collection, filters, sorts)
        self.assertEqual(len(data), 2, "Should have 2 documents but have %d" % len(data))
        self.assertEqual(data[0]['date'], "This TEST date", "Sort is not correct")

if __name__ == '__main__':
    unittest.main()

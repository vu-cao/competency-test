# -*- coding: utf-8 -*-
import sys
import os.path
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from isentia.spiders.isentiaspider import IsentiaSpider
import responses


class IsentiaSpiderTestCase(unittest.TestCase):
    def setUp(self):
        self.response = response = responses.fake_response_from_file(
            'fakeresponse.html', "http://www.bbc.com/news/election-us-2016-35649252")
        self.spider = IsentiaSpider()

    def test_parse_items(self):
        """ Test case for parse_items method
        :return:
        """
        results = self.spider.parse_items(self.response)
        for item in results:
            self.assertEqual(item['domain'], "bbc.com", "Domain is not correct")
            self.assertEqual(item['link'], "http://www.bbc.com/news/election-us-2016-35649252", "Link is not correct")
            self.assertEqual(item['headline'], "After Nevada: Five (unlikely) ways Trump can still be stopped",
                             "Headline is not correct")
            self.assertEqual(item['author'], "Anthony Zurcher", "Author is not correct")
            self.assertEqual(item['introduction'],
                             "There was one clear winner after Tuesday's Nevada caucus - Donald Trump.",
                             "Introduction is not correct")
            self.assertEqual(item['category'], "US Election 2016", "Category is not correct")
            self.assertIsNotNone(item['content'], "Content has to be not empty")

    def test_get_base_domain(self):
        """ Test case for get_base_domain method
        :return:
        """
        url = "http://www.google.com.au/calendar"
        self.assertEqual(self.spider.get_base_domain(url), "google.com.au", "Base domain is not correct")

        url = "http://yahoo.com.au/test"
        self.assertEqual(self.spider.get_base_domain(url), "yahoo.com.au", "Base domain is not correct")

if __name__ == '__main__':
    unittest.main()
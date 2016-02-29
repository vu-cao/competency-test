# -*- coding: utf-8 -*-
import sys
import os.path
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from isentia.spiders.IsentiaSpider import IsentiaSpider
import responses


class IsentiaSpiderTestCase(unittest.TestCase):
    def setUp(self):
        self.spider = IsentiaSpider()

    def test_parse_items(self):
        response = responses.fake_response_from_file('fakeresponse.html', "http://www.bbc.com/news/election-us-2016-35649252")
        results = self.spider.parse_items(response)
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

if __name__ == '__main__':
    unittest.main()
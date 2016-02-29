# -*- coding: utf-8 -*-
import re
import sys
import os.path

from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from spiderutils.itemutils import ItemUtils


class IsentiaSpiderFollowlinksSpider(CrawlSpider):
    """ A spider for isentia competency test"""

    # Spider name
    name = "isentia_follow_links"
    # Domain to crawl
    allowed_domains = settings['WEB_DOMAIN']
    # url to start
    start_urls = settings['WEB_START_URLS']

    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(settings['FOLLOWING_LINK_PATTERNS']))),
            callback="parse_items",
            process_links="filter_links",
            follow = True),
    )

    def filter_links(self, links):
        if not settings['FOLLOW_LINK']:
            return []
        else:
            return links

    def parse_start_url(self, response):
        """ Override this method to include urls in start_urls
        :param response: response
        :return:
        """
        return self.parse_items(response)

    def parse_items(self, response):
        """ The overriden function to parse response

        :param response: Response to parse
        :return: NewsItem
        """

        selectors = Selector(response).xpath(settings['FIELD_ROOT_NODE'])

        for selector in selectors:
            yield ItemUtils.parse(selector, response)

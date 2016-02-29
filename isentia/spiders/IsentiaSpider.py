# -*- coding: utf-8 -*-
import sys
import os.path

import scrapy
from scrapy.selector import Selector
from scrapy.conf import settings

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from spiderutils.itemutils import ItemUtils


class IsentiaSpider(scrapy.Spider):
    """ A spider for isentia competency test"""

    # Spider name
    name = "isentia"
    # Domain to crawl
    allowed_domains = settings['WEB_DOMAIN']
    # url to start
    start_urls = settings['WEB_START_URLS']

    def parse(self, response):
        """ The overriden function to parse response
        :param response: Response to parse
        :return: NewsItem
        """
        selectors = Selector(response).xpath(settings['FIELD_ROOT_NODE'])

        for selector in selectors:
            yield ItemUtils.parse(selector, response)


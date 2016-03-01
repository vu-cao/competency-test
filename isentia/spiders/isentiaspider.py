# -*- coding: utf-8 -*-
import re

from urlparse import urlparse

from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from isentia.items import NewsLoader
from isentia.items import NewsItem


class IsentiaSpider(CrawlSpider):
    """ A spider for isentia competency test"""

    # Spider name
    name = "isentia"
    # Domain to crawl
    allowed_domains = settings['WEB_DOMAIN']
    # url to start
    start_urls = settings['WEB_START_URLS']

    rules = (
        Rule(LinkExtractor(
            allow=(re.compile(settings['FOLLOWING_LINK_PATTERNS']))),
            callback="parse_items",
            process_links="filter_links",
            follow=True),
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

        # If not include start urls, don't need to parse response from start_urls
        if settings['START_URLS_INCLUDED']:
            return self.parse_items(response)

    def parse_items(self, response):
        """ The overriden function to parse response

        :param response: Response to parse
        :return: NewsItem
        """

        selectors = Selector(response).xpath(settings['FIELD_ROOT_NODE'])

        for selector in selectors:
            yield self.parse_response(selector, response)

    def get_base_domain(self, url):
        """ Return base domain from url
        :param url: url used to retrieve base domain
        :return: Base domain
        """
        base = urlparse(url).netloc
        if base.upper().startswith("WWW."):
            base = base[4:]

        # drop any ports
        base = base.split(':')[0]
        return base

    def parse_response(self, selector, response):
        """ Parse response and load item retrieving from response
        :param selector: Selector used to extract data from response
        :param response: Response from scrapping
        :return: News Item
        """
        loader = NewsLoader(NewsItem(), selector)
        loader.add_value('domain', self.get_base_domain(response.url))
        loader.add_value('link', response.url)
        loader.add_xpath('headline', settings['FIELD_HEADLINE_NODE'])
        loader.add_xpath('author', settings['FIELD_AUTHOR_NODE'])
        loader.add_xpath('date', settings['FIELD_DATE_NODE'])
        loader.add_xpath('category', settings['FIELD_CATEGORY_NODE'])
        loader.add_xpath('introduction', settings['FIELD_INTRODUCTION_NODE'])
        loader.add_xpath('content', settings['FIELD_CONTENT_NODE'])

        return loader.load_item()

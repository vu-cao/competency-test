# -*- coding: utf-8 -*-
import scrapy
import urlparse
import re
from isentia.items import NewsItem
from scrapy.conf import settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import log

class IsentiaSpiderFollowlinksSpider(CrawlSpider):
    """ A spider for isentia competency test"""

    # Spider name
    name = "isentia_follow_links"
    # Domain to crawl
    allowed_domains = [settings['WEB_DOMAIN']]
    # url to start
    start_urls = settings['WEB_START_URLS']
    # xPath text
    text = "/text()"
    # url for the current response
    response_url = ""

    rules = (
        Rule(LinkExtractor(allow=(re.compile(settings['FOLLOWING_LINK_PATTERNS']),)),
             callback="parse_items",
             follow=True),
    )

    def parse_start_url(self, response):
        """ Override this method to include urls in start_urls
        :param response: response
        :return:
        """
        self.response_url = response.url
        return self.parse_items(response)


    def filter_links(self, links):
        """ Method to convert relative url to absolute url
        :param links: Links contained in the current response
        :return: Filtered links
        """
        self.logger.info("FILTER_LINKS")
        self.logger.info(self.response_url)

        filtered_links = []
        for link in links:
            self.logger.info(link)
            filtered_links.append(urlparse.urljoin(self.response_url, link))
        return filtered_links

    def append(self, xPath):
        """ Method to append self.text into xPath

        :param xPath: xPath to be appended
        :return: Appended xPath
        """
        return xPath + self.text

    def parse_items(self, response):
        """ The overriden function to parse response

        :param response: Response to parse
        :return: NewsItem
        """

        data = response.xpath(settings['FIELD_ROOT_NODE'])

        for d in data:
            news = NewsItem()

            news['domain'] = self.allowed_domains
            news['link'] = response.url
            news['headline'] = d.xpath(self.append(settings['FIELD_HEADLINE_NODE'])).extract_first()

            news['author'] = d.xpath(self.append(settings['FIELD_AUTHOR_NODE'])).extract_first()
            news['date'] = d.xpath(settings['FIELD_DATE_NODE']).extract_first()

            news['category'] = d.xpath(self.append(settings['FIELD_CATEGORY_NODE'])).extract_first()

            news['introduction'] = d.xpath(self.append(settings['FIELD_INTRODUCTION_NODE'])).extract_first()

            paragraphs = d.xpath(settings['FIELD_CONTENT_NODE'])
            content = ""
            for paragraph in paragraphs:
                paragraph_content = paragraph.xpath(".").extract()[0]
                content += paragraph_content + "\n"

            news['content'] = content

            return news

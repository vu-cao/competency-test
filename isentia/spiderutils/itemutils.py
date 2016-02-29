# -*- coding: utf-8 -*-
from urlparse import urlparse
from isentia.items import NewsItem
from scrapy.conf import settings


class ItemUtils(object):
    # xPath text
    text = "/text()"

    @classmethod
    def append(cls, xPath):
        """ Method to append cls.text into xPath

        :param xPath: xPath to be appended
        :return: Appended xPath
        """
        return xPath + cls.text

    @classmethod
    def get_base_domain(cls, url):
        """
        :param url: url used to retrieve base domain
        :return: Base domain
        """
        base = urlparse(url).netloc
        if base.upper().startswith("WWW."):
            base = base[4:]

        # drop any ports
        base = base.split(':')[0]
        return base

    @classmethod
    def parse(cls, selector, response):
        news = NewsItem()

        news['domain'] = cls.get_base_domain(response.url)
        news['link'] = response.url
        news['headline'] = selector.xpath(cls.append(settings['FIELD_HEADLINE_NODE'])).extract_first()

        news['author'] = selector.xpath(cls.append(settings['FIELD_AUTHOR_NODE'])).extract_first()
        news['date'] = selector.xpath(settings['FIELD_DATE_NODE']).extract_first()

        news['category'] = selector.xpath(cls.append(settings['FIELD_CATEGORY_NODE'])).extract_first()

        news['introduction'] = selector.xpath(cls.append(settings['FIELD_INTRODUCTION_NODE'])).extract_first()

        paragraphs = selector.xpath(settings['FIELD_CONTENT_NODE'])
        content = ""
        for paragraph in paragraphs:
            paragraph_content = paragraph.xpath(".").extract()[0]
            content += paragraph_content + "\n"

        news['content'] = content

        return news

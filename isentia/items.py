# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import string
import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Compose, MapCompose
from scrapy.utils.markup import remove_tags
from scrapy.utils.markup import replace_entities


from scrapy.conf import settings

class NewsItem(scrapy.Item):
    """ Scrapy item for news """

    domain = scrapy.Field()
    link = scrapy.Field()
    headline = scrapy.Field()

    date = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    introduction = scrapy.Field()
    category = scrapy.Field()

    # def __repr__(self):
    #     """only print out headline after exiting the Pipeline"""
    #     return repr({"headline": self['headline']})


class NewsLoader(ItemLoader):
    """ Item loader for News item """

    def filter_content(content):
        """ Convert content from list to string. Paragraphs are separate by '\n'
        :param content: Content of news in list format
        :return: String converted from list
        """
        return '\n'.join(content)

    def convert_date(content):
        """ Convert date data in string format to datetime data
        :param content: Content of date field in list format
        :return: Datetime data
        """
        result = content
        # Default date format is %d %B %Y
        date_format = "%d %B %Y"

        if content:
            result = datetime.datetime.strptime(content[0], settings['DATE_FORMAT'] or date_format)

        return result

    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_tags, replace_entities, string.strip)

    content_out = Compose(filter_content)
    date_out = Compose(convert_date)

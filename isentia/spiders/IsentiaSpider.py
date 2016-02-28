import scrapy
from scrapy.selector import Selector
from isentia.items import NewsItem
from scrapy.conf import settings

class IsentiaSpider(scrapy.Spider):
    """ A spider for isentia competency test"""

    # Spider name
    name = "isentia"
    # Domain to crawl
    allowed_domains = settings['WEB_DOMAIN']
    # url to start
    start_urls = settings['WEB_START_URLS']
    # xPath text
    text = "/text()"

    @classmethod
    def append(self, xPath):
        return xPath + self.text

    def parse(self, response):
        """ The overriden function to parse response
        :param response: Response to parse
        :return: NewsItem
        """
        data = Selector(response).xpath(settings['FIELD_ROOT_NODE'])

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

            yield news
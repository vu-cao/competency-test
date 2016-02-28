# -*- coding: utf-8 -*-

# Scrapy settings for isentia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'isentia'

SPIDER_MODULES = ['isentia.spiders']
NEWSPIDER_MODULE = 'isentia.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'isentia (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'isentia.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'isentia.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'isentia.pipelines.SomePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

DOWNLOAD_DELAY = 5

# Set pipeline for scrapping.
# CleanupHTMLPipeline is used to clean html tags in content
# MongoDBPipeline is used to save data into MongoDB
ITEM_PIPELINES = ["isentia.pipelines.CleanupHTMLPipeline", "isentia.pipelines.MongoDBPipeline"]

# MongoDB settings
MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "isentia"
MONGODB_COLLECTION = "news"

# Settings for website
# Domain
WEB_DOMAIN = "bbc.com"
# Urls to start
WEB_START_URLS = ["http://www.bbc.com/news/election-us-2016-35649252",
                  "http://www.bbc.com/news/world-middle-east-35674908"]

# Settings for fields to be scrapped. The settings are XPath expression
# This is the top level we will look into
FIELD_ROOT_NODE = "//*/div[@class='column--primary']/div[@class='story-body']"
# Node for headline
FIELD_HEADLINE_NODE = ".//h1[@class='story-body__h1']"
# Node for author
FIELD_AUTHOR_NODE = ".//span[@class='byline__name']"
# Node for date
FIELD_DATE_NODE = ".//div[@class='story-body__mini-info-list-and-share']/ul/li[@class='mini-info-list__item']/div/@data-datetime"
# Node for category
FIELD_CATEGORY_NODE = ".//div[@class='story-body__mini-info-list-and-share']/ul/li[@class='mini-info-list__item']/a[@class='mini-info-list__section']"
#Node for introduction
FIELD_INTRODUCTION_NODE = ".//div[@class='story-body__inner']/p[@class='story-body__introduction']"
# Node for content
FIELD_CONTENT_NODE = ".//div[@class='story-body__inner' and @property='articleBody']/*[self::p|self::h1|self::h2|self::h3|self::h4][text()]"

# Settings for following links
# Do you want to follow link?
FOLLOW_LINK = True
# Depth limit to follow links. 0 is unlimited
DEPTH_LIMIT = 2
# Patterns for following links. The pattern is in regular expression
# FOLLOWING_LINK_PATTERNS = "\/news(\/.)*\/.+-\d{8}$"
FOLLOWING_LINK_PATTERNS = "\/news\/.*\d{8}$"

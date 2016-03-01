# Data Engineer Competency Test Solution

----------

## Purpose #
Provide solution for the [Data Engineer Competency Test](https://github.com/abhishek-isentia/Competency-Test/blob/master/Data-Engineer-Test.md)

## Frameworks Used##


- [scrapy](www.scrapy.org) 1.0.5
- pymongo 3.2.1
- [mongomock](https://pypi.python.org/pypi/mongomock/2.0.0) 2.0.0
- [web.py](http://webpy.org/) 0.37


## Folder Structure ##
- api: API to retrieve data which were scrapped and stored in MongoDB 
- isentia: scrapy code
- mongomock: mongomock library
- tests: Unit test cases
	- responses: Mock response for scrapy code test
- utils: Utilities classes

## Important classes ##
- `isentia.spiders.isentiaspider.IsentiaSpider`: Scrapy spider class to scrap information
- `isentia.items.NewsItem`: News model.
- `isentia.items.NewsLoader`: Loader to populate data into NewsItem
- `isentia.pipelines.MongoDBPipeline`: Pipeline which is used to save News into MongoDB
- `utils.mongodbutils.MongoDBUtils`: Utilities class supporting MongoDB operations
- `api.news`: Module contains classes for REST API.

## Solution ##


## Configuration settings ##
- `DOWNLOAD_DELAY`: Delay time between 2 requests. Default is 5 seconds
- `MONGODB_SERVER`: Address of MongoDB. Default is `aws-us-east-1-portal.14.dblayer.com`. This is [compose.io](http://compose.io) server
- `MONGODB_PORT`: Port number of MongoDB. Default is `10208`
- `MONGODB_DB`: MongoDB database name. Default is `isentia`
- `MONGODB_COLLECTION`: MongoDB collection name. Default is `news`
- `MONGODB_USER`: MongoDB user name.
- `MONGODB_PASSWORD`: MongoDB password
- `WEB_DOMAIN`: List of allowed domains to scrap. This is a list
- `WEB_START_URLS`: List of urls which scrapy will start scrapping.
- `FIELD_ROOT_NODE`: XPath expression of a node in web page. This node will contains all nodes which contains information we need to extract.
- `FIELD_HEADLINE_NODE`: XPath expression of node contains headline information.
- `FIELD_AUTHOR_NODE`: XPath expression of node contains author information.
- `FIELD_DATE_NODE`: XPath expression of node contains date information.
- `FIELD_CATEGORY_NODE`: XPath expression of node contains category information.
- `FIELD_INTRODUCTION_NODE`: XPath expression of node contains introduction information.
- `FIELD_CONTENT_NODE`: XPath expression of nodes contains main content.
- `DATE_FORMAT`: Format of date
- `START_URLS_INCLUDED`: True if you want to scrap urls in WEB\_START\_URLS; False if not
- `FOLLOW_LINK`: True if you want to follow links in a page.
- `DEPTH_LIMIT`: Number of levels you want to follow.
- `FOLLOWING_LINK_PATTERNS`: Regular expression patterns of links to follow. Scrapy only follow a link if it matches these patterns 

## Execution ##
1. **Scrapping web:**
	1. Go to `isentia` folder
	2. Execute `scrapy crawl isentia`
2. **Unit test**
	
	1. To run all test cases
		- Go to root folder
		- Execute `python -m unittest discover`


	- To execute a particular test case 
		1. Go to `tests`
		2. Execute `python <name of python file>`. For example, `python testisentiaspider.py` 
3. **API**
	1. Go to `api` folder
	2. Start server: Execute `python news.py [ip address:port]`. For example, `python news 127.0.0.1:8000` will start server on `127.0.0.1 (localhost)`, port `8000`. If not specify, IP address is 172.0.0.1 and port is 8080
	3. To search for domain (`bbc.com`), execute: `http://localhost:8080/news/domain/bbc.com`
	4. To search for url (http://bbc.com/news), execute: `http://localhost:8080/news/url/http:%2F%2Fwww.bbc.com%2Fnews`. Note: Remember to encode url value.
	5. To search for both domain and url (bbc.com and url has `news`), execute: `http://localhost:8080/news/domain/bbc.com/url/news`
import sys
import os.path

import web
import pymongo

import json

import settings

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.mongodbutils import MongoDBUtils


urls = (

    '/news/domain/(.*)', 'DomainSearch',
    '/news/url/(.*)', 'UrlSearch',
    '/news/domain/(.*)/url/(.*)', 'UrlSearch'
)


class IsentiaApplication(web.application):
    """ Subclass web.application to set default address 127.0.0.1 """
    def run(self, port=settings.SERVER_PORT, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, (settings.SERVER_ADDRESS, port))


class News(object):
    """ Model class """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Base(object):
    """ Base class for REST API """
    def connect(self):
        """ Connect to MongoDB and return collection
        :return: MongoDB collection
        """
        connection_string = MongoDBUtils.create_connection_string(
                settings.MONGODB_SERVER, settings.MONGODB_PORT,
                settings.MONGODB_USER, settings.MONGODB_PASSWORD)
        client = MongoDBUtils.connect(connection_string)
        collection = MongoDBUtils.get_collection(client, settings.MONGODB_DB, settings.MONGODB_COLLECTION)

        return collection

    def format(self, results):
        """ Format result from MongoDB to JSON
        :param results: JSON data contains list of News
        :return:
        """
        jsons = []

        # Default date format is %d %B %Y
        date_format = "%d %B %Y"

        for result in results:
            args = {}
            for key in result:
                if key == 'date':
                    # Convert BSON datetime to string
                    value = result['date'].strftime(settings.DATE_FORMAT or date_format)
                    args.update({key: value})
                else:
                    args.update({key: result[key]})
            jsons.append(News(**args))

        return jsons


class DomainSearch(Base):
    """ REST API for search by domain """
    def GET(self, domain):
        collection = super(DomainSearch, self).connect()
        # Search MongoDB collection using domain input, sort by date ascending
        results = MongoDBUtils.search(collection, {'domain': domain}, [('date', pymongo.ASCENDING)])
        print "DOMAIN"
        print domain
        jsons = super(DomainSearch, self).format(results)
        return json.dumps([news.__dict__ for news in jsons])


class UrlSearch(Base):
    """ REST API for search by url """
    def GET(self, url):
        collection = super(UrlSearch, self).connect()
        # Search MongoDB collection using url input, sort by date ascending
        print url
        results = MongoDBUtils.search(collection, {'link': url}, [('date', pymongo.ASCENDING)])

        jsons = super(UrlSearch, self).format(results)
        return json.dumps([news.__dict__ for news in jsons])


class DomainUrlSearch(Base):
    """ REST API for search by both domain and url """
    def GET(self, domain, url):
        collection = super(DomainUrlSearch, self).connect()

        # Create filter for MongoDB query
        filters = {}
        if domain:
            filters.update({'domain': domain})
        if url:
            filters.update({'link': url})

        # Search MongoDB collection using domain and url inputs, sort by date ascending
        results = MongoDBUtils.search(collection, filters, [('date', pymongo.ASCENDING)])

        jsons = super(DomainUrlSearch, self).format(results)
        return json.dumps([news.__dict__ for news in jsons])

if __name__ == "__main__":
    app = IsentiaApplication(urls, globals())
    app.run()
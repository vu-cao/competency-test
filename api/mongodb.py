# -*- coding: utf-8 -*-

import sys
import os.path
import getopt
import pymongo

import json
from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scrapy.conf import settings
from utils.mongodbutils import MongoDBUtils


date_format = "%d %B %Y"


class News(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

""" The API to retrieve news from MongoDB """


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hd:u:", ["help", "domain=", "url="])
        except getopt.error, msg:
             raise Usage(msg)

        domain = ""
        url = ""

        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                print "mongodb.py -d <domain> -u <url>"
                return
            elif opt in ('-d', '--domain'):
                domain = arg
            elif opt in ('-u', '--url'):
                url = arg

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

    connection_string = MongoDBUtils.create_connection_string(
        settings['MONGODB_SERVER'], settings['MONGODB_PORT'],
        settings['MONGODB_USER'], settings['MONGODB_PASSWORD'])
    client = MongoDBUtils.connect(connection_string)
    collection = MongoDBUtils.get_collection(client, settings['MONGODB_DB'], settings['MONGODB_COLLECTION'])

    filters = {}
    if domain:
        filters.update({'domain': domain})
    if url:
        filters.update({'link': url})
    sorts = [('date', pymongo.ASCENDING)]
    results = MongoDBUtils.search(collection, filters, sorts)

    jsons = []
    for result in results:
        args = {}
        for key in result:
            if key == 'date':
                value = result['date'].strftime(date_format)
                args.update({key: value})
            else:
                args.update({key: result[key]})
        jsons.append(News(**args))
        print json.dumps([news.__dict__ for news in jsons])


if __name__ == "__main__":
    sys.exit(main())

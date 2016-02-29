# -*- coding: utf-8 -*-

import sys
import os.path
import getopt


from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scrapy.conf import settings
from utils.mongodbutils import MongoDBUtils


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
    collection = MongoDBUtils.connect(connection_string, settings['MONGODB_DB'], settings['MONGODB_COLLECTION'])

    print MongoDBUtils.search(collection, domain, url)


if __name__ == "__main__":
    sys.exit(main())

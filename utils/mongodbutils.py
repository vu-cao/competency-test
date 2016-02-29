# -*- coding: utf-8 -*-
import pymongo


class MongoDBUtils(object):
    @classmethod
    def create_connection_string(cls, server, port, username, password):
        """ Create connection string from parameters
        :param server: MongoDB server name
        :param port: MongoDB port number
        :param username: MongoDB username
        :param password: MongoDB password
        :return: Connection string which can be used later
        """

        print port
        return "mongodb://" + username + ':' + password + '@' + server + ':' + str(port)

    @classmethod
    def connect(cls, uri, db, collection):
        """ Connect MongoDB with input parameters
        :param server: MongoDB server name
        :param port: MongoDB port number
        :param database: MongoDB database name
        :param collection: MongoDB collection name
        :return: collection object
        """
        client = pymongo.MongoClient(uri)
        db = client[db]
        return db[collection]

    @classmethod
    def search(cls, collection, domain, url):
        """ Search MongoDB with input criteria
        :param domain: Criteria to filter
        :param url: Criteria to filter
        :param collection: Collection to retrieve data from
        :return: List of JSON object
        """

        condition = {}
        if domain:
            condition['domain'] = {'$regex': domain}
        if url:
            condition['link'] = {'$regex': url}

        cursor = collection.find({'link': {'$regex': url}}, {'_id': False}).sort([
            ('date', pymongo.ASCENDING)
        ])

        print "Total records: %d" % cursor.count()
        return list(cursor)

# -*- coding: utf-8 -*-
import pymongo


class MongoDBUtils(object):
    """ Utility class to support operation with MongoDB """

    @classmethod
    def create_connection_string(cls, server, port, username, password):
        """ Create connection string from parameters
        :param server: MongoDB server name
        :param port: MongoDB port number
        :param username: MongoDB username
        :param password: MongoDB password
        :return: Connection string which can be used later
        """

        return "mongodb://" + username + ':' + password + '@' + server + ':' + str(port)

    @classmethod
    def connect(cls, uri):
        """ Connect MongoDB with input parameters
        :param server: MongoDB server name
        :param port: MongoDB port number
        :param database: MongoDB database name
        :param collection: MongoDB collection name
        :return: MongoClient object
        """
        return pymongo.MongoClient(uri)

    @classmethod
    def get_collection(cls, client, database, collection):
        db = client[database]
        return db[collection]

    @classmethod
    def search(cls, collection, filters, sorts):
        """ Search MongoDB with input criteria
        :param collection: Collection to search
        :param filters: Dictionary contains criteria to filter
        :param sorts: List contains criteria to sort
        :return: List of JSON object
        """

        condition = {}
        for key in filters:
            condition[key] = {'$regex': filters[key]}

        cursor = collection.find(condition, {'_id': False}).sort(sorts)

        return list(cursor)

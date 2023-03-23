import mongomock
from os import environ
from pymongo import MongoClient


class DatabaseService:
    '''
    Database connection generator
    '''

    def __init__(self) -> None:
        self.client = MongoClient(environ.get('DB_CONN_STRING'))
        self.db = self.client[environ.get('DB_NAME')]


class MockDatabase:
    '''
    Database service used for testing
    '''

    def __init__(self) -> None:
        self.client = mongomock.MongoClient()
        self.db = self.client['test']
        self.db['users'].insert_one({
            'firstName': 'Existent',
            'lastName': 'User',
            'email': 'iexists@putsbox.com',
            'apiKey': 'fakeapikey'
        })

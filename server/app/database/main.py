from pymongo import MongoClient
from pymongo.collection import Collection
import os

class Database:
    ''' MongoDB interface '''

    DEFAULT_DB = os.environ.get('MONGODB_DEFAULT_DB', 'db')
    DEFAULT_COLLECTION = os.environ.get('MONGODB_DEFAULT_COLLECTION', 'data')

    CONNECTION = None

    def __init__(self,database:str=None, collection:str=None):
        self.database = database
        self.collection = collection


    def connect(self, database:str=None, collection:str=None) -> Collection:
        ''' Connect to a database and collection 

            `database` defualts to the `MONGODB_DEFAULT_DB` environmental variable if not passed

            `collection` defualts to the `MONGODB_DEFAULT_COLLECTION` environmental variable if not passed
        
        '''
        if not database:   database   = os.environ.get('MONGODB_DEFAULT_DB', 'db') if not self.database else self.database
        if not collection: collection = os.environ.get('MONGODB_DEFAULT_COLLECTION', 'data') if not self.collection else self.collection

        auth_str = os.environ.get('MONGODB_HOSTNAME', 'localhost')
        if os.environ.get('MONGODB_USERNAME') and os.environ.get('MONGODB_PASSWORD'):
            auth_str = f"{os.environ.get('MONGODB_USERNAME')}:{os.environ.get('MONGODB_PASSWORD')}@" + auth_str

        if not self.CONNECTION:
            self.CONNECTION = MongoClient(f'mongodb://{auth_str}:27017/')

        return self.CONNECTION.get_database(database).get_collection(collection)


    def disconnect(self):
        ''' Disconnect from a database and collection '''

        if self.CONNECTION:
            self.CONNECTION.close()
            self.CONNECTION = None


    def __enter__(self) -> Collection:
       return self.connect()
       
    def __exit__(self, exception_type, exception_value, traceback):
        self.disconnect()
    


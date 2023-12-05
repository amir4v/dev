from functools import partial

from pymongo import MongoClient
from bson import ObjectId


class DictToClass:
    def __init__(self, d):
        d = d or {}
        self.d = d
        for key, value in d.items():
            setattr(self, key, value)
    
    @property
    def dict(self):
        """TODO: Convert class attributes to key-value dict."""
        class my_dict(dict):
            cls = object
            def __init__(self, *args, **kwargs):
                self.cls = object
                super().__init__(*args, **kwargs)
        
        self.d = my_dict(self.d)
        self.d.cls = self
        return self.d


class MongoModel:
    HOST = 'localhost'
    PORT = 27017
    # use admin [THEN] db.createUser({user:'admin', pwd: '123456', roles:['userAdminAnyDatabase']})
    USERNAME = 'admin'
    PASSWORD = '123456'
    #
    AUTH_MECHANISM = 'DEFAULT'
    
    def __init__(self, db,
                       host=HOST, port=PORT,
                       username=USERNAME, password=PASSWORD,
                       authMechanism=AUTH_MECHANISM,
                       connection_string=None):
        self.client = self.get_client(host, port,
                                      username, password,
                                      authMechanism,
                                      connection_string)
        self.db = self.get_db(db)
        self.reset_collections()
    
    def reset_collections(self):
        for collection in self.db.list_collection_names():
            setattr(self, collection, self.get_collection(collection))
    
    def get_client(self, host=HOST, port=PORT,
                         username=USERNAME, password=PASSWORD,
                         authMechanism=AUTH_MECHANISM,
                         connection_string=None,
                         db=None, collection=None):
        """
        authMechanism must be in ('MONGODB-OIDC', 'MONGODB-CR', 'PLAIN',
                                  'SCRAM-SHA-1', 'MONGODB-X509', 'DEFAULT',
                                  'SCRAM-SHA-256', 'GSSAPI', 'MONGODB-AWS').
        PyMongo automatically uses  'SCRAM-SHA-1'.
        """
        if connection_string:
            self.client = MongoClient(connection_string)
        else:
            self.client = MongoClient(
                host=host,
                port=port,
                username=username,
                password=password,
                authMechanism=authMechanism,
            )
        
        if db and collection:
            self.db = self.client[db]
            self.reset_collections()
            return self.db[collection]
        elif db:
            self.db = self.client[db]
            self.reset_collections()
            return self.client[db]
        else:
            return self.client
    
    def get_db(self, db):
        self.db = self.client[db]
        self.reset_collections()
        return self.db
    
    def get_collection(self, collection, db=None):
        if db:
            self.db = self.client[db]
            self.reset_collections()
        collection = self.db[collection]
        collection.get = partial(self.get, collection=collection)
        return collection
    
    def get(self, _id, collection, cls=False):
        obj = collection.find_one({'_id': ObjectId(_id)})
        if cls:
            obj = obj or {}
            return DictToClass(obj)
        return obj

import json
from functools import partial

from pymongo import MongoClient
import bson
from bson import ObjectId
from rest_framework import renderers
from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS
)


class DjangoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            result = super().default(o)
        except:
            result = str(o)
        return result


class DRFRenderer(renderers.JSONRenderer):
    """
    Renderer which serializes to JSON.
    """
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b''
        
        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)
        
        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS
        
        ret = json.dumps(
            data, cls=DjangoJSONEncoder,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )
        
        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: https://gist.github.com/damncabbage/623b879af56f850a6ddc
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()


class DictToClass:
    def __init__(self, d):
        d = d or {}
        self.d = d
        for key, value in d.items():
            setattr(self, key, value)
    
    @property
    def dict(self):
        """TODO: Convert class attributes to key-value dict (to be always fresh and update to the last changes to the class)."""
        class my_dict(dict):
            cls = object
            def __init__(self, *args, **kwargs):
                self.cls = object
                super().__init__(*args, **kwargs)
        
        self.d = my_dict(self.d)
        self.d.cls = self
        return self.d


class MongoModel:
    """
    * If you want to relate a Document to another, you have to use _id=ObjectId('...') of that Document
        to a field named like that Collection in your Document and your field can be a ObjectId or a list and
        in that list you put some ObjectId.
    * So two point:
        field name (referenced Collection)
        value (ObjectId)
    """
    
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
    
    def get(self, _id=None, cls=False, **kwargs):
        """
        This get function retrieves a document from a MongoDB collection
        based on the _id field. The function uses the find_one method
        to retrieve the document. If the _id field is not provided,
        the function retrieves the first document that matches the
        query parameters. The function then uses the $lookup operator to
        join the document with other collections based on the fields
        that contain ObjectId values. Finally, the function returns the
        document as a dictionary or as an object of a specified class,
        depending on the value of the cls parameter.
        """
        collection = kwargs.pop('collection', None)
        
        if kwargs:
            obj = collection.find_one(kwargs) or {}
        else:
            obj = collection.find_one({'_id': ObjectId(_id)}) or {}
        
        # ### TODO: problem: it's slower ### #
        pairs = {}
        obj.pop('_id', None) # To prevent self-recursion
        
        for k, v in obj.items():
            if isinstance(v, ObjectId):
                pairs[k] = v
            elif isinstance(v, list):
                pass
            elif isinstance(v, dict):
                pass
        
        pipeline = [
            {'$match':
                kwargs or {'_id': ObjectId(_id)}},
            {'$limit': 1}
        ]
        
        for k, v in pairs.items():
            pipeline.append(
                {'$lookup': {
                    'from': k,
                    'localField': k,
                    'foreignField': '_id',
                    'as': k
                }}
            )
        
        obj = collection.aggregate(pipeline)
        obj = list(obj)
        obj.append({}) # in case of an empty query result
        obj = obj[0]
        obj['_id'] = obj.get('_id') # to make a default 'None' value for '_id' field
        
        if cls:
            return DictToClass(obj)
        return obj

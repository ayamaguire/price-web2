import uuid
from src.common import database
from src.common import constants as dbc
from src.models.stores import exceptions as StoresExceptions


class Store(object):

    def __init__(self, name, domain, tag_name, query, _id=None):
        self.name = name
        self.domain = domain
        self.tag_name = tag_name
        self.query = query
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return "<Store {} with domain {}>".format(self.name, self.domain)

    def make_json(self):
        json = {dbc.NAME: self.name,
                dbc.DOMAIN: self.domain,
                dbc.TAG_NAME: self.tag_name,
                dbc.QUERY: self.query,
                dbc.SELF_ID: self._id}
        return json

    def save_to_db(self):
        database.Database.update(collection=dbc.STORES,
                                 query={dbc.SELF_ID: self._id},
                                 data=self.make_json())

    @classmethod
    def get_by_id(cls, _id):
        data = database.Database.find_one(collection=dbc.STORES, query={dbc.SELF_ID: _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_name(cls, name):
        data = database.Database.find_one(collection=dbc.STORES, query={dbc.NAME: name})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_domain(cls, domain):
        data = database.Database.find_one(collection=dbc.STORES, query={dbc.DOMAIN: {'$regex': '^{}'.format(domain)}})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_url(cls, url):
        for i in range(14, len(url)+1):
            search = list(database.Database.find(collection=dbc.STORES,
                                                 query={dbc.DOMAIN: {'$regex': '^{}'.format(url[:i])}}))
            if len(search) == 1:
                return cls(**search[0])
        raise StoresExceptions.StoreNotFoundError(message="The store {} did not match any existing stores.".format(url))

    @classmethod
    def get_all(cls):
        data = database.Database.find(collection=dbc.STORES, query={})
        return [cls(**elem) for elem in data]

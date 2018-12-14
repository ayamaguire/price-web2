from bs4 import BeautifulSoup
import requests
import re
import uuid

from src.common import database
from src.common import constants as dbc
from src.models.stores import store
from src.models.items import exceptions as ItemExceptions


class Item(object):

    def __init__(self, name, url, _id=None):
        self.name = name
        self.url = url
        self.store = store.Store.get_by_url(self.url)
        self.price = None
        # self.load_price()
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return "<Item {} with url {}>".format(self.name, self.url)

    def make_json(self):
        json = {dbc.NAME: self.name,
                dbc.URL: self.url,
                dbc.SELF_ID: self._id
                }
        return json

    def save_to_db(self):
        database.Database.update(collection=dbc.ITEMS,
                                 query={dbc.SELF_ID: self._id},
                                 data=self.make_json())

    @classmethod
    def get_by_id(cls, _id):
        data = database.Database.find_one(collection=dbc.ITEMS, query={dbc.SELF_ID: _id})
        if data is not None:
            return cls(**data)

    def load_price(self):
        page = requests.get(self.url)
        content = page.content
        soup = BeautifulSoup(content, 'html.parser')
        element = soup.find(self.store.tag_name, self.store.query)
        if element is None:
            raise ItemExceptions.InvalidPriceError(message="Price element could not be located."
                                                           "Please check item URL, store tag name, and store query.")
        string_price = element.text.strip()

        # need to extract the price that is ##.## without $ or other symbols
        pattern = re.compile('(\d+\.+\d+)')
        match = pattern.search(string_price)
        self.price = float(match.group())
        return self.price

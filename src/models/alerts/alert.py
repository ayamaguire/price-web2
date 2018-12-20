import uuid
import requests
import datetime

from src.common import database
from src.common import constants as dbc
from src.models.alerts import constants
from src.models.items import item
from src.models.users import user


class Alert(object):

    def __init__(self, user_email, item_id, price_limit, last_checked=None, last_price=None, user_id=None, _id=None):
        self.user_email = user_email
        self.item_id = item_id
        self.item = item.Item.get_by_id(self.item_id)
        self.price_limit = float(price_limit)
        self.last_checked = last_checked or datetime.datetime.utcnow()
        self.last_price = last_price
        self.user_id = user_id or user.User.get_by_email(user_email)._id
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return "<Alert for {} on item {} with price limit {}.>".format(self.user_email, self.item.name, self.price_limit)

    def make_json(self):
        json = {dbc.USER_EMAIL: self.user_email,
                dbc.ITEM_ID: self.item_id,
                dbc.PRICE_LIMIT: self.price_limit,
                dbc.LAST_CHECKED: self.last_checked,
                dbc.LAST_PRICE: self.last_price,
                dbc.USER_ID: self.user_id,
                dbc.SELF_ID: self._id}
        return json

    def save_to_db(self):
        database.Database.update(collection=dbc.ALERTS,
                                 query={dbc.SELF_ID: self._id},
                                 data=self.make_json())

    def remove(self):
        """" Deletes the instance from the db."""
        database.Database.remove(collection=dbc.ALERTS,
                                 query={dbc.SELF_ID: self._id})

    @classmethod
    def get_by_id(cls, _id):
        data = database.Database.find_one(collection=dbc.ALERTS, query={dbc.SELF_ID: _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_email(cls, email):
        data = database.Database.find(collection=dbc.ALERTS, query={dbc.USER_EMAIL: email})
        return [cls(**elem) for elem in data]

    @classmethod
    def get_by_user_id(cls, user_id):
        data = database.Database.find(collection=dbc.ALERTS, query={dbc.USER_ID: user_id})
        return [cls(**elem) for elem in data]

    @classmethod
    def update_alerts_email(cls, user_id, new_email):
        alerts_to_update = cls.get_by_user_id(user_id=user_id)
        for elem in alerts_to_update:
            elem.user_email = new_email
            elem.save_to_db()

    def send(self):
        return requests.post(constants.URL,
                             auth=("api", constants.API_KEY),
                             data={"from": constants.FROM,
                                   "to": self.user_email,
                                   "subject": constants.SUBJECT.format(self.item.name),
                                   "text": "The price on your item is now at or below {}. Link: {}".format(
                                       self.price_limit, self.item.url)
                                   }
                             )

    @classmethod
    def find_needing_update(cls, elapsed=constants.ELAPSED):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(seconds=elapsed)
        data = database.Database.find(collection=dbc.ALERTS, query={dbc.LAST_CHECKED: {'$lte': last_updated_limit}})
        return [cls(**elem) for elem in data]

    def update_price(self):
        self.last_price = self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_db()

    def send_if_price_reached(self):
        if self.item.price <= self.price_limit:
            return self.send()


def check_alerts():
    alerts = Alert.find_needing_update()
    for alert in alerts:
        alert.update_price()
        return alert.send_if_price_reached()

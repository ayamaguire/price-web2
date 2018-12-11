import uuid

from src.common import database, utils
from src.common import constants as dbc
from src.models.users import exceptions as UserExceptions


class User(object):

    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = utils.Utils.encrypt_password(password)
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return "<User {}.>".format(self.email)

    def make_json(self):
        json = {dbc.EMAIL: self.email,
                dbc.PASSWORD: self.password,
                dbc.SELF_ID: self._id}
        return json

    def save_to_db(self):
        database.Database.insert(collection=dbc.USERS,
                                 data=self.make_json())

    @classmethod
    def get_by_id(cls, _id):
        data = database.Database.find_one(collection=dbc.USERS, query={dbc.SELF_ID: _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def register_user(cls, email, password):
        """
        Takes the given email, asserts that it isn't already in the database, and adds the new user to the db if it isn't.
        :param email: user email
        :param password: sha512 hashed password
        :return: True if we were able to register the user, error if else
        """
        user_data = database.Database.find_one(collection=dbc.USERS,
                                               query={dbc.EMAIL: email})
        if user_data is not None:
            # user is already registered
            raise UserExceptions.UserAlreadyRegisteredError(message="The user {} is already registered.".format(email))
        if not utils.Utils.email_is_valid(email):
            # the given email is not of good email form, raise some kind of error
            raise UserExceptions.InvalidEmailError(message="{} is not a valid email.".format(email))
        cls(email, password).save_to_db()
        return True

    @staticmethod
    def user_valid(email, password):
        """
        A static method for checking whether an email/password combo is valid.
        TODO: create similar methods for retrieving email, password, etc
        :param email: A user email
        :param password: A sha512 hashed password
        :return: True if valid, False if not.
        """
        user_data = database.Database.find_one(collection=dbc.USERS, query={dbc.EMAIL: email})
        if user_data is None:
            # the given email does not correspond to a user in the database
            raise UserExceptions.UserDoesNotExistError(message="The user {} does not exist".format(email))
        if not utils.Utils.check_hashed_password(password, user_data[dbc.PASSWORD]):
            # The email given was ok, but the password didn't match
            raise UserExceptions.IncorrectPasswordError(message="The given password is incorrect.")
        return True

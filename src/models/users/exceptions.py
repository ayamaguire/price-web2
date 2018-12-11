# user errors


class UserError(Exception):
    def __init__(self, message):
        self.message = message


class UserDoesNotExistError(UserError):
    """ Exception for when a given email is not in the database."""


class IncorrectPasswordError(UserError):
    """ Exception for when given password doesn't match database for given user. """


class InvalidEmailError(UserError):
    """ Exception for when the given email is not valid format. """


class UserAlreadyRegisteredError(UserError):
    """ Exception for when the given user is already registered and cannot be re-registered. """

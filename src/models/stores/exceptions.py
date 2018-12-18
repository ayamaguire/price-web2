
class StoreException(Exception):
    def __init__(self, message):
        self.message = message


class StoreNotFoundError(StoreException):
    """ URL does not relate to an existing store."""


class StoreAlreadyExistsError(StoreException):
    """ Error for when store is already in database"""

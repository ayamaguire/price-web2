
class ItemsException(Exception):
    def __init__(self, message):
        self.message = message


class InvalidPriceError(ItemsException):
    """ Price could not be found on website with given span and tag. """

from passlib.hash import pbkdf2_sha512
import re

from src.common import database


class Utils(object):

    @staticmethod
    def encrypt_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login or register forms
        :return: A pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches what's in the database
        :param password: Sha512 hashed password the user gave
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def email_is_valid(email):
        """
        Ensure the given email is of valid format
        :param str email: Email to validate
        :return: True if email is str@str.str, False otherwise
        """
        email_match = re.compile('^([\w-]+\.)+[\w]+@([\w-]+\.)+[\w]+$')
        return email_match.match(email) is not None

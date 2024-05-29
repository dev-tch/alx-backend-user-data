#!/usr/bin/env python3
"""authentification  module
"""
import bcrypt
from db import DB, NoResultFound, InvalidRequestError
from user import User


def _hash_password(password: str) -> bytes:
    """ return bytes from string password """
    # here we must encode string password to bytes
    # because bcrypt works with bytes
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ register new user """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email=email,
                                     hashed_password=hashed_password)
        except InvalidRequestError:
            raise
        raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """validate password for registred user"""
        try:
            user_obj = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'),
                              user_obj.hashed_password):
                return True
        except (NoResultFound, InvalidRequestError):
            pass
        return False

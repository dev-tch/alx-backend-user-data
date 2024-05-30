#!/usr/bin/env python3
"""authentification  module
"""
import bcrypt
from db import DB, NoResultFound, InvalidRequestError
from user import User
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """ return bytes from string password """
    # here we must encode string password to bytes
    # because bcrypt works with bytes
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """ return session id"""
        try:
            obj_user = self._db.find_user_by(email=email)
            token_session = _generate_uuid()
            self._db.update_user(obj_user.id, session_id=token_session)
            return token_session
        except (NoResultFound, InvalidRequestError):
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ return the user that having session_id"""
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: int) -> None:
        """ remove session id from user """
        try:
            user_obj = self._db.find_user_by(id=user_id)
            self._db.update_user(user_obj.id, session_id=None)
        except (NoResultFound, InvalidRequestError):
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        update reset_token with new uuid if user exists
        """
        try:
            user_obj = self._db.find_user_by(email=email)
            uuid = _generate_uuid()
            self._db.update_user(user_obj.id, reset_token=uuid)
        except (NoResultFound, InvalidRequestError):
            raise ValueError

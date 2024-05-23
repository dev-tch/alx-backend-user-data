#!/usr/bin/env python3
""" module to manage session"""
from api.v1.auth.auth import Auth
import uuid
import os


class SessionAuth(Auth):
    """ implement class SessionAuth"""
    # create a class attribute
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates Session ID"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ return user_id based on session_id"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None):
        """ returns a cookie value from a request"""
        if request is None:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        if cookie_name is None:
            return None
        return request.cookies.get(cookie_name)

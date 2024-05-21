#!/usr/bin/env python3
""" module for BASIC authentication method"""
from api.v1.auth.auth import Auth
from flask import request
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ implement class BasicAuth"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ base64 encode"""
        if any([authorization_header is None,
                not isinstance(authorization_header, str)]):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """ base64 decode"""
        part_base64 = base64_authorization_header
        if part_base64 is None:
            return None
        if not isinstance(part_base64, str):
            return None
        try:
            byte_decoded = base64.b64decode(part_base64)
            # convert byte to string UTF-8
            utf8_str = byte_decoded.decode('UTF-8')
            return utf8_str
        except (UnicodeDecodeError, base64.binascii.Error):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """ extract user auth data"""
        auth_val = decoded_base64_authorization_header
        valid_str = auth_val is None or not isinstance(auth_val, str)
        if valid_str or ':' not in auth_val:
            return (None, None)
        return tuple(auth_val.split(':', 1))

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ return object User from credentials"""
        if any([
            not isinstance(user_email, str),
            not isinstance(user_pwd, str)
        ]):
            return None
        try:
            list_usr_instance = []
            list_usr_instance = User.search({'email': user_email})
            if len(list_usr_instance) == 0:
                return None
            else:
                for obj_user in list_usr_instance:
                    if obj_user.is_valid_password(user_pwd):
                        return obj_user
                return None
        except KeyError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ override the  method current_user in super class Auth"""
        auth_value = self.authorization_header(request)
        if not auth_value:
            return None
        part_64auth = self.extract_base64_authorization_header(auth_value)
        if not part_64auth:
            return None
        utf8_str = self.decode_base64_authorization_header(part_64auth)
        if not utf8_str:
            return None
        email, passwd = self.extract_user_credentials(utf8_str)
        if email is None or passwd is None:
            return None
        # finally return the object User from credentials
        return self.user_object_from_credentials(email, passwd)

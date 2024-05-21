#!/usr/bin/env python3
""" module for BASIC authentication method"""
from api.v1.auth.auth import Auth
from flask import request
import base64


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

#!/usr/bin/env python3
""" module for BASIC authentication method"""
from api.v1.auth.auth import Auth
from flask import request


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

#!/usr/bin/env python3
""" module authentication"""
from flask import request
from typing import List
from typing import TypeVar


class Auth:
    """implement class Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """handle authentication """
        auth_req_ok = all([
            path is None,
            not excluded_paths,

        ])
        if auth_req_ok:
            return True
        if path in excluded_paths:
            return False
        if not path.endswith('/'):
            path += '/'
        for path_ignored in excluded_paths:
            if not path_ignored.endswith('/'):
                path_ignored += '/'
            if path == path_ignored:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """handle Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ handle current User """
        return None

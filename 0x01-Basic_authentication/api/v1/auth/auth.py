#!/usr/bin/env python3
""" module authentication"""
from flask import request
from typing import List
from typing import TypeVar


class Auth:
    """implement class Auth"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """handle authentication """
        return False

    def authorization_header(self, request=None) -> str:
        """handle Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ handle current User """
        return None

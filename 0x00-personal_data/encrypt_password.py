#!/usr/bin/env python3
""" module using bcrypt"""
from typing import TypeVar
import bcrypt


T = TypeVar('T', str, bytes)


def hash_password(password: str) -> T:
    """ hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

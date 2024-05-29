#!/usr/bin/env python3
"""authentification  module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """ return bytes from string password """
    # here we must encode string password to bytes
    # because bcrypt works with bytes
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed

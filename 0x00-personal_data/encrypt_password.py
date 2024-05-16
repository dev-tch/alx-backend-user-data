#!/usr/bin/env python3
""" module using bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

#!/usr/bin/env python3
""" module using bcrypt"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password):
    """ validates password with hashed value"""
    hashed = hash_password(password)
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

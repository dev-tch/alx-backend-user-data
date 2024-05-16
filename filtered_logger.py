#!/usr/bin/env python3
"""
module with one function filter_datum
"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """return log message obfuscated
    Inputs:
    *fields:
    list of strings representing all fields to obfuscate
    *redaction:
    a string representing by what the field will be obfuscated
    *message:
    string representing the log line
    *separator:
    string representing by which character
    is separating all fields in the log line
    """
    # join fields with or operator
    rgx_choose_field = '|'.join(fields)
    rgx_not_sep = '[^{}]+'.format(separator)
    pattern = r'({}){}{}'.format(rgx_choose_field, rgx_not_sep, separator)
    # \1 replace  replaced with first group of pattern
    # we have to add '=' to replacement because first group contain only field
    replacement = r'\1={}{}'.format(redaction, separator)
    return re.sub(pattern, replacement, message)

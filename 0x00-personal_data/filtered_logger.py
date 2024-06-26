#!/usr/bin/env python3
"""
module with:
* one function filter_datum
* class RedactingFormatter

"""
import re
from typing import List
import logging
import mysql.connector
import os


PII_FIELDS = ("name", "email", "ssn", "phone", "password")


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self._fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ string representation of Loging record"""
        record.msg = filter_datum(self._fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """ return logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(fields=PII_FIELDS)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ connect to mysql database and return MySQLConnection object"""
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "holberton")
    try:
        cnx = mysql.connector.connect(
            user=db_user,
            password=db_pwd,
            host=db_host,
            database=db_name,
        )
        return cnx
    except mysql.connector.Error:
        return None


def main():
    """fetch data from table users and log it"""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    columns = list(map(lambda x: x[0], cursor.description))
    rows = cursor.fetchall()
    for row in rows:
        _list = [f"{tup_obj[0]}={tup_obj[1]}" for tup_obj in zip(columns, row)]
        message = f'{RedactingFormatter.SEPARATOR} '.join(_list)
        message += f'{RedactingFormatter.SEPARATOR}'
        logger.info(filter_datum(PII_FIELDS, RedactingFormatter.REDACTION,
                                 message, RedactingFormatter.SEPARATOR))

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()

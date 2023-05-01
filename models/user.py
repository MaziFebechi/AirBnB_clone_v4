#!/usr/bin/python3
"""
    This contains the class called User
"""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import hashlib


class User(BaseModel, Base):
    """
        The representation of the class called user
    """
    __tablename__ = 'users'
    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",
                              cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        """
            To return hashed password
        """
        return self._password

    @password.setter
    def password(self, value):
        """
            The fset the password with hash is presented
        """
        self._password = hashlib.md5(value.encode('utf8')).hexdigest()

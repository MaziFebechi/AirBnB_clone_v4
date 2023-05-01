#!/usr/bin/python3
"""
    The BaseModel class module is defined here
"""
from os import getenv
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """   
        Here is the fundamental BaseModel class on which other classes depend on
    """
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
    """
        Initializing some public instance attributes.
    """
    if (len(kwargs) == 0):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    else:
        if kwargs.get("created_at"):
            kwargs["created_at"] = datetime.strptime(
                kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.created_at = datetime.now()
        if kwargs.get("created_at"):
            kwargs["updated_at"] = datetime.strptime(
                kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
        else:
            self.updated_at = datetime.now()
        for key, val in kwargs.items():
            if "__class__" not in key:
                steattr(self, key, val)
        if not self.id:
            self.id = str(uuid.uuid())

    def __str__(self):
        """
           The string representation of the BaseModel class is shown here
        """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def __repr__(self):
        """
           To return the string representation of BaseModel class
        """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def save(self):
        """
            To save the updated_at attribute with the name new.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self, save_to_disk=False):
        """
            Returning the dictionary representation of BaseModel class.
        """
        cp_dct = dict(self.__dict__)
        cp_dct['__class__'] = self.__class__.__name__
        cp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        if hasattr(self, "_sa_instance_state"):
            del cp_dct["_sa_instance_state"]
        if cp_dct['__class__'] is "User" and not save_to_disk:
            cp_dct.pop("_password", None)
        return (cp_dct)

    def delete(self):
        """
            Deleting an object
        """
        models.storage.delete(self)

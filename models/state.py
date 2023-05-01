#!/usr/bin/python3
"""
   The class called State is contained below
"""
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models


class State(BaseModel, Base):
    """
        The state class is presentd here.
        The relationship between state and city is created.
    """
     __tablename__ = "states"

    if getenv ("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            """
                To return a list of instances of city if city.state_id==current stste.id
                The filestorage relationship between state and city
            """
            list_cities = []
            for city in models.storage.all("city").values():
                if city.state_id == self.id:
                    list_cities.append(city)
            return list_cities

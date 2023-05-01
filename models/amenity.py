#!/usr/bin/python3
"""
    The class Amenity is contained in this file
"""
from os import getenv
from models.base_model import BaseModel, Base
from model.place import place_amenity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
        Representation of Amenities
    """
    __tablename__= "amenities"
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        place_amenities = relationship("place", secondary=place_amenity,
                                        back_populates="amenities")
    else:
        name = ""

#!/usr/bin/python3
"""Model that defines a class 'basemodel' """


from uuid import uuid4
from datetime import datetime
from copy import deepcopy

from . import storage


class BaseModel:
    """ class called basemodel"""

    format = "%y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *_, **kwargs):
        """constructor function"""

        if len(kwargs) != 0:
            for m, n in kwargs.items():
                if m != "__class__":
                    if m == "created_at" or m == "updated_at":
                        setattr(self, m, 
                                datetime.strptime(n, BaseModel.format))
                    else:
                        setattr(self, m, n)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = deepcopy(self.created_at)
            storage.new(self)

    def save(self):
        """Save the object"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Return a dictionary"""
        dot = {}

        dot.update(self.__dict__)
        dot["__class__"] = self.__class__.__name__
        dot["created_at"] = self.created_at.strftime(BaseModel.format)
        dot["updated_at"] = self.updated_at.strftime(BaseModel.format)

        return dot

    def __str__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

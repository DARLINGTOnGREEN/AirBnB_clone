#!/usr/bin/python3
"""Module that defines a class 'filestorage' """
import json


class FileStorage:
    """class FileStorage"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return all the objects"""
        return FileStorage.__objects

    def new(self, obj):
        """set obj in __objects"""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """serialize __objects to JSON file"""
        dot = {}

        for m, n in FileStorage.__objects.items():
            dot[m] = n.to_dict()

        with open(FileStorage.__file_path, "w") as file:
            json.dump(dot, file)

    def reload(self):
        """Deserialize from __file_path to __objects"""
        from models.base_model import BaseModel

        dot = None
        try:
            with open(self.__file_path, "r") as file:
                dot = json.load(file)

            for m, n in dot.items():
                self.__objects[m] = BaseModel(**n)
        except Exception:
            pass

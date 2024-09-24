#!/usr/bin/python3
"""Unittest for models/base_model.py"""


import unittest
from datetime import datetime
from time import sleep
from uuid import UUID
from model.base_models import BaseModel


class TestBaseModel(unittest.TestCase):
    """test case for the BaseModel class"""

    def test_instance_creation(self):
        """Test if a BaseModel instance is created successfully"""
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)

    def test_it_type(self):
        """Test if the id is of type string and is a valid UUID"""
        obj = BaseModel()
        self.assertIsInstance(obj.id, str)
        # check if the id is a valid UUID
        try:
            UUID(obj.id, version=4)
        except ValueError:
            self.fail(f"{obj.id} is not a valid UUID")

    def test_created_at_type(self):
        """Test if created_at is of type datetime"""
        obj = BaseModel()
        self.assertIsInstance(obj.created_at, datetime)

    def test_updated_at_type(self):
        """Test if updated_at is of type datetime and
        equal to created_at"""
        obj = BaseModel()
        self.assertIsInstance(obj.updated_at, datetime)
        self.assertEqual(obj.updated_at, obj.created_at)

    def test_save_method(self):
        """Test the save method to ensure it
        updates the updated_at attribute"""
        obj = BaseModel()
        old_updated_at = obj.updated_at
        sleep(0.1)
        obj.save()
        new_updated_at = obj.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertGreater(new_updated_at, old_updated_at)

    def test_to_dict(self):
        """Test the to_dict method returns a dictionary
        and contains the correct data"""
        obj = BaseModel()
        obj_dict = obj.to_dict()
        self.assertIsInstance(obj_dict, dict)
        # Check if mandatory keys exist
        self.assertIn('id', obj_dict)
        self.assertIn('created_At', obj_dict)
        self.assertIn('updated_at', obj_dict)
        self.assertIn('__class__', obj_dict)
        # Check if they are in ISO format
        # ie 'created_at and Updated_at'
        self.assertIsInstance(obj_dict['created_at'], str)
        self.assertIsInstance(obj_dict['updated_at'], str)
        try:
            datetime.strptime(obj_dict['created_at'], BaseModel.format)
            datetime.strptime(obj_dict['updated_at'], BaseModel.format)
        except ValueError:
            self.fail("created_at or updated_at format is incorrect")

    def test_str_method(self):
        """Test the __str__ method to ensure correct output format"""
        obj = BaseModel()
        obj_str = str(ob)
        expected = f"[BaseModel] ({obj.id}) {obj.__dict__}"
        self.assertEqual(obj_str,  expected)


if __name__ == "__main__":
    unittest.main()

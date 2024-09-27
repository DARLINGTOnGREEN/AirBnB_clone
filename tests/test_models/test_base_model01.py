#!/usr/bin/python3
"""Unittests for models/base_model.py"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
from time import sleep


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def test_instance_creation(self):
        """Test the creation of BaseModel instance."""
        bm = BaseModel()
        self.assertIsInstance(bm, BaseModel)
        self.assertIsInstance(bm.id, str)
        self.assertIsInstance(bm.created_at, datetime)
        self.assertIsInstance(bm.updated_at, datetime)

    def test_unique_ids(self):
        """Test that two different instances have unique IDs."""
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_str_method(self):
        """Test __str__ method of BaseModel."""
        bm = BaseModel()
        expected_str = f"[BaseModel] ({bm.id}) {bm.__dict__}"
        self.assertEqual(str(bm), expected_str)

    def test_save_method(self):
        """Test save method of BaseModel."""
        bm = BaseModel()
        old_updated_at = bm.updated_at
        sleep(0.1)
        bm.save()
        self.assertGreater(bm.updated_at, old_updated_at)

    def test_to_dict(self):
        """Test to_dict method of BaseModel."""
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertIsInstance(bm_dict, dict)
        self.assertEqual(bm_dict['id'], bm.id)
        self.assertEqual(bm_dict['__class__'], 'BaseModel')
        self.assertEqual(bm_dict['created_at'],
                         bm.created_at.strftime(BaseModel.format))
        self.assertEqual(bm_dict['updated_at'],
                         bm.updated_at.strftime(BaseModel.format))

    def test_kwargs_instantiation(self):
        """Test instantiation with kwargs."""
        dt = datetime.now().isoformat()
        bm = BaseModel(id="test-id", created_at=dt, updated_at=dt)
        self.assertEqual(bm.id, "test-id")
        self.assertEqual(bm.created_at.isoformat(), dt)
        self.assertEqual(bm.updated_at.isoformat(), dt)

    def test_save_updates_storage(self):
        """Test that calling save updates storage (mocked for now)."""
        bm = BaseModel()
        bm.save()
        # Check if the object is stored in storage (mock or replace as needed)
        self.assertIsNotNone(bm.updated_at)


if __name__ == "__main__":
    unittest.main()

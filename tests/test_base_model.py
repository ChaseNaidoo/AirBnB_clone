#!/usr/bin/python3
"""Unit test for BaseModel"""
import unittest
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Tests covering initialization, string representation,
    saving, and dictionary conversion methods.

    Methods:
        - test_initialization: Tests the initialization of a BaseModel instance
        - test_string_representation: Tests the string representation.
        - test_saving: Tests the saving method of a BaseModel instance.
        - test_to_dict: Tests the to_dict method of a BaseModel instance.
    """

    def test_initialization(self):
        my_model = BaseModel()
        self.assertTrue(isinstance(my_model, BaseModel))
        self.assertTrue(hasattr(my_model, 'id'))
        self.assertTrue(hasattr(my_model, 'created_at'))
        self.assertTrue(hasattr(my_model, 'updated_at'))

    def test_string_representation(self):
        my_model = BaseModel()
        expected_str = "[BaseModel] ({}) {}".format(my_model.id,
                                                    my_model.__dict__)
        self.assertEqual(str(my_model), expected_str)

    def test_saving(self):
        my_model = BaseModel()
        initial_updated_at = my_model.updated_at
        my_model.save()
        self.assertNotEqual(my_model.updated_at, initial_updated_at)

    def test_to_dict(self):
        my_model = BaseModel()
        my_model_dict = my_model.to_dict()
        self.assertTrue(isinstance(my_model_dict, dict))
        self.assertEqual(my_model_dict['__class__'], 'BaseModel')
        self.assertEqual(my_model_dict['created_at'],
                         my_model.created_at.isoformat())
        self.assertEqual(my_model_dict['updated_at'],
                         my_model.updated_at.isoformat())
        self.assertTrue('id' in my_model_dict)


if __name__ == '__main__':
    unittest.main()

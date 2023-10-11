#!/usr/bin/python3
"""Class User hat inherits from BaseModel"""
from models.base_model import BaseModel

class User(BaseModel):
    """User class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""

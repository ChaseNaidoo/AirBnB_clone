#!/usr/bin/python3
"""Class BaseModel"""
import uuid
from datetime import datetime
import models

class BaseModel:
    """Base model for common attributes/methods"""

    def __init__(self, *args, **kwargs):
        """Initialize BaseModel instance"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self,
                            key,
                            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f'))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """Return a string representation of the instance"""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(
            class_name, self.id, self.__dict__
        )

    def save(self):
        """Update the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance"""
        result = dict(self.__dict__)
        result['__class__'] = self.__class__.__name__
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result

#!/usr/bin/python3
"""The FileStorage class"""
import json
import os


class FileStorage:
    """Represent an abstracted storage engine.

    Attributes:
        __file_path (str): The name of the file to save Objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj class name>.id"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        objdict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists."""
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as f:
                objdict = json.load(f)
                for key, value in objdict.items():
                    class_name = value["__class__"]
                    del value["__class__"]
                    obj = eval(class_name)(**value)
                    self.new(obj)

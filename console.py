#!/usr/bin/python3
"""The command interpreter"""
import cmd
import sys
import shlex
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command processor"""
    cmd.Cmd.completekey = None
    prompt = "(hbnb) "

    def __init__(self):
        super().__init__()
        self.l_classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review
        }

    def preloop(self):
        """Disables raw input to handle non-interactive input"""
        if not sys.stdin.isatty():
            self.use_rawinput = False
        
    def postloop(self):
        """Cleanup or actions needed after the command loop has completed."""
        if not sys.stdin.isatty():
            print()

    def lookup_instance(self, args):
        """Find and return an instance based on class name and ID"""
        if len(args) < 2:
            raise ValueError("** class name missing **")

        class_name, obj_id = args[0], args[1].strip('"')
        cls = self.l_classes.get(class_name)
        if cls is None:
            raise ValueError(f"** class {class_name} doesn't exist **")

        objects = storage.all()
        for obj in objects.values():
            if obj.id == obj_id and isinstance(obj, cls):
                return obj

        raise ValueError("** no instance found **")

    def do_show(self, arg):
        """Shows string representation of an instance passed"""
        try:
            args = arg.split()
            if len(args) == 0:
                raise ValueError("** class name missing **")
            class_name = args[0]
            if class_name not in self.l_classes:
                raise ValueError("** class doesn't exist **")
            if len(args) < 2:
                raise ValueError("** instance id missing **")
            instance_id = args[1].strip('"')
            instance = self.lookup_instance(args)
            print(instance)
        except ValueError as e:
            print(e)

    def do_destroy(self, arg):
        """Deletes an instance passed"""
        try:
            args = arg.split()
            instance = self.lookup_instance(args)
            key_to_delete = None
            for key, obj in storage.all().items():
                if obj is instance:
                    key_to_delete = key
                    break
            if key_to_delete:
                del storage.all()[key_to_delete]
                storage.save()
            else:
                raise ValueError("** no instance found **")
        except ValueError as e:
            print(e)

    def do_create(self, type_model):
        """Creates an instance according to a given class"""
        try:
            if not type_model:
                raise ValueError("** class name missing **")

            cls = self.l_classes.get(type_model)
            if cls is None:
                raise ValueError("** class doesn't exist **")

            instance = cls()
            instance.save()
            print(instance.id)
        except ValueError as e:
            print(e)

    def do_all(self, arg):
        """Prints string representation of all instances of a given class"""
        try:
            if not arg:
                raise ValueError("** class name missing **")

            args = arg.split()
            if args[0] not in self.l_classes:
                raise ValueError("** class doesn't exist **")

            objects = storage.all()
            instances = [str(obj) for obj in objects.values()
                         if isinstance(obj, self.l_classes[args[0]])]
            print(instances)
        except ValueError as e:
            print(e)

    def do_update(self, arg):
        """Updates an instance based on the class name and
        id by adding or updating attribute (save the change into the JSON file)
        """
        try:
            if not arg:
                raise ValueError("** class name missing **")

            a = ""
            for argv in arg.split(','):
                a = a + argv

            args = shlex.split(a)

            if args[0] not in self.l_classes:
                raise ValueError("** class doesn't exist **")
            if len(args) == 1:
                raise ValueError("** instance id missing **")

            objects = storage.all()
            for obj in objects.values():
                if obj.id == args[1].strip('"') and isinstance(obj,
                                                               self.l_classes[args[0]]):
                    if len(args) == 2:
                        raise ValueError("** attribute name missing **")
                    elif len(args) == 3:
                        raise ValueError("** value missing **")

                    setattr(obj, args[2], args[3])
                    storage.save()
                    return
            raise ValueError("** no instance found **")
        except ValueError as e:
            print(e)

    def help_help(self):
        """Prints help command description"""
        print("Provides description of a given command")

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_quit(self, line):
        """Quit command to exit the command interpreter"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the command interpreter"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()

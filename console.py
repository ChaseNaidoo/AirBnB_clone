#!/usr/bin/python3
"""The command interpreter"""
import cmd
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

    prompt = "(hbnb) "

    l_classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review,
        'count': None
    }

    def default(self, line):
        """Handle unknown commands:
        <class name>.all()
        <class name>.count()
        <class name>.show(<id>)
        <class name>.destroy(<id>)
        <class name>.update(<id>, <attribute name>, <attribute value>)
        """
        if line.endswith(".all()"):
            class_name = line[:-6]
            self.do_all(class_name)
        elif line.endswith(".count()"):
            class_name = line[:-7]
            self.do_count(class_name)
        elif line.startswith("User.show(") and line.endswith('")'):
            class_name, id_part = line.split(".show(")
            instance_id = id_part.strip(')"')
            self.do_show(f"{class_name} {instance_id}")
        elif line.startswith("User.destroy(\"") and line.endswith('")'):
            class_name, id_part = line.split(".destroy(\"")
            instance_id = id_part.strip('")')
            self.do_destroy(f"{class_name} {instance_id}")
        elif line.startswith("User.update(") and line.endswith(')'):
            self.do_update(line)
        else:
            print(f"*** Unknown command: {line} ***")

    def lookup_instance(self, args):
        """Find and return an instance based on class name and ID."""
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
        """Shows string representation of an instance passed."""
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
        """Deletes an instance passed."""
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
        """Creates an instance according to a given class."""
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
            class_name = args[0]

            if class_name not in self.l_classes:
                raise ValueError("** class doesn't exist **")

            objects = storage.all()
            instances = [str(obj) for obj in objects.values()
                         if isinstance(obj, self.l_classes[class_name])]
            print(instances)
        except ValueError as e:
            print(e)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        """
        try:
            args = shlex.split(arg)
            if len(args) < 4:
                raise ValueError("** Usage: <class name>.update(<id>, <attribute name>, <attribute value>) **")

            class_name = args[0]
            instance_id = args[1].strip('"')

            if class_name not in self.l_classes:
                raise ValueError(f"** class {class_name} doesn't exist **")

            objects = storage.all()
            for obj in objects.values():
                if obj.id == instance_id and isinstance(obj, self.l_classes[class_name]):
                    attribute_name = args[2]
                    attribute_value = args[3]

                    if hasattr(obj, attribute_name):
                        setattr(obj, attribute_name, attribute_value)
                        storage.save()
                        return
                    else:
                        raise ValueError(f"** no attribute '{attribute_name}' found **")

            raise ValueError("** no instance found **")
        except ValueError as e:
            print(e)

    def do_count(self, arg):
        """Prints the count of instances of a given class using <class name>.count()"""
        try:
            if not arg:
                raise ValueError("** class name missing **")

            class_name = arg.split('.')[0]

            if class_name not in self.l_classes:
                raise ValueError(f"** class {class_name} doesn't exist **")

            objects = storage.all()
            count = len([obj for obj in objects.values() if isinstance(obj, self.l_classes[class_name])])
            print(count)
        except ValueError as e:
            print(e)

    def help_help(self):
        """Prints a description of a given command."""
        print("Provides a description of a given command")

    def emptyline(self):
        """Do nothing when an empty line is entered."""
        pass

    def do_quit(self, line):
        """Quit command to exit the command interpreter."""
        return True

    def do_EOF(self, line):
        """EOF command to exit the command interpreter."""
        return True

    
if __name__ == '__main__':
    HBNBCommand().cmdloop()

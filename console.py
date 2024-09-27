#!/usr/bin/python3
"""Module that defines HBNBCommand class"""


import cmd
from models.base_model import BaseModel
from models import storage
import re


class HBNBCommand(cmd.Cmd):
    """this is the console class"""

    prompt = "(hbnb) "

    def do_quit(self, _):
        """ to exit console"""
        return True

    def do_EOF(self, _):
        """ctrl+D to quit"""
        return True

    def emptyline(self):
        """creates emptylines"""
        pass

    def do_create(self, line):
        """Creates a new instance of basemodel"""
        args = line.split(" ")
        print(args, len(args))
        if line == "":
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        else:
            obj = BaseModel()
            print(obj.id)
            storage.save()

    def do_show(self, line):
        """Prints the string representation of an

        instance based on the class name and id"""
        args = line.split(" ")
        if line == "":
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        else:
            o = None
            for _, n in storage.all().items():
                if n.id == args[1]:
                    o = n
                    break

            print(o) if o is not None else print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        args = line.split(" ")
        if line == "":
            print("** class name missing **")
        elif args[0] != "BaseModel":
            print("** class doesn't exist **")
        elif len(args) != 2:
            print("** instance id missing **")
        else:
            o = None
            for _, n in storage.all().items():
                if n.id == args[1]:
                    o = n
                    break

            if o is not None:
                del storage.all()[f"{o.__class__.__name__}.{o.id}"]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation of all instances"""
        args = line.split(" ")

        if line != "" and line == "BaseModel":
            # print the basemode object
            all = storage.all()
            all_list = []
            for m, n in all.items():
                if type(n) is BaseModel:
                    all_list.append(n)

            print("[", end="")
            for idx in range(len(all_list)):
                print(all_list[idx], end="")
                if idx + 1 == len(all_list):
                    print("]")
                else:
                    print(", ", end="")

        elif line == "":
            # print all objects
            pass
        elif line != "" and line != "BaseModel":
            # class doesn't exist
            pass

    def do_update(self, line):
        """Updates an instance based on the class name and id"""
        args = re.findall(r'(\S+)|"([^"]+)"', line)
        args = [item[0] if item[0] else item[1] for item in args]

        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] != "BaseModel":
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"

        if key not in storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        obj = storage.all()[key]
        attr_name = args[2]
        attr_value = args[3]

        # prevent updating id, created_at, and updated_at
        if attr_name in ["id", "created_at", "updated_at"]:
            print(f"** cannot update {attr_name} **")
            return

        # Case  the attribute value to the appropriate type
        current_value = getattr(obj, attr_name, None)
        if current_value is not None:
            # if the attribute exist
            try:
                if isinstance(current_value, int):
                    attr_value = int(attr_value)
                elif isinstance(current_value, float):
                    attr_value = float(attr_value)
            except ValueError:
                print(f"** cannot cast {attr_value} to "
                      f"{type(current_value).__class__.__name__} **")

        # Update the attribute and save the object
        setattr(obj, attr_name, attr_value)
        obj.save()
        print(f"Updated {attr_name} for {args[1]} to {attr_value}")


if __name__ == "__main__":
    HBNBCommand().cmdloop()

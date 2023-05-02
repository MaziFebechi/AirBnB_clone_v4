#!/usr/bin/python3
"""
    To define class FileStorage
"""
import json
import models


class FileStorage:
    """
        For Serializes instances to JSON file and deserializes to JSON file.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
            To return the dictionary
        """
        new_dict = {}
        if cls is None:
            return self.__objects

        if cls != "":
            for k, v in self.__objects.items():
                if cls == k.split(".")[0]:
                    new_dict[k] = v
            return new_dict
        else:
            return self.__objects

    def new(self, obj):
        """
            To set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An object instance.
        """
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        """
            Serialization __objects attribute to JSON file.
        """
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        """
            Here we deserialize the JSON file to __objects.
        """
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
            To deletes an obj
        '''
        if obj is not None:
            key = str(obj.__class__.__name__) + "." + str(obj.id)
            FileStorage.__objects.pop(key, None)
            self.save()

    def close(self):
        '''
            To deserialize JSON file to objects
        '''
        self.reload()

    def get(self, cls, id):
        '''
            To retrieve an obj w/class name and id
        '''
        result = None

        try:
            for v in self.__objects.values():
                if v.id == id:
                    result = v
        except BaseException:
            pass

        return result

    def count(self, cls=None):
        '''
            Now count num objects in FileStorage
        '''
        cls_counter = 0

        if cls is not None:
            for k in self.__objects.keys():
                if cls in k:
                    cls_counter += 1
        else:
            cls_counter = len(self.__objects)
        return cls_counter

from model import User, Places, Country, Reviews, Amenities, City
from abc import ABC, abstractmethod
import json
from file_handler import file_handler
import os

class IPersistenceManager(ABC):
    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def get(self, entity_id, entity_type):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id, entity_type):
        pass


class DataManager(IPersistenceManager):
    def save(self, entity):
        entity = entity.to_dict()
        action = file_handler(entity["type"])
        if action == 5:
            print("There is no such entity")
        else:
            data = self.get(entity["type"])
            with open(action, 'w') as filename:
                data.append(entity)
                json.dump(data, filename)
        print("File saved")
        return 0

    def get(self, entity_type, entity_id=None):
        action = file_handler(entity_type) 
        if action == 5:
            print("There is no such type entity")
        else:
            if not os.path.exists(action):
                with open(action, 'w') as filename:
                    return []
            with open(action, 'r') as filename:
                if os.path.getsize(action) == 0:
                    return []
                data = json.load(filename)
                if entity_id == None:
                    return data
                for datum in data:
                    if datum["id"] == entity_id:
                        return datum
        return None
    
    def update(self, entity_id, entity_type, attribute, value):
        action = file_handler(entity_type)
        if action == 5:
            print("There is no such type entity")
        else:
            data = self.get(entity_type)
            with open(action, "w") as filename:
                for datum in data:
                    if datum["id"] == entity_id:
                        datum[attribute] = value
                json.dump(data, filename)
                    

    def delete(self, entity_id, entity_type):
        action = file_handler(entity_type)
        if action == 5:
            print("There is no such type entity")
        else:
            data = self.get(entity_type)
            with open(action, "w") as filename:
                for index, datum in enumerate(data):
                    if datum["id"] == entity_id:
                        del data[index]
                json.dump(data, filename)

class PresentationLayer:
    def __init__(self, dm):
        self.dm = dm

    def save(self, entity):
        self.dm.save(entity)

    def get(self, entity_type, entity_id=None):
        get = self.dm.get(entity_type, entity_id)
        return get

    def get_country(self, code):
        countries = self.dm.get("Country")
        for country in countries:
            if country["code"] == code:
                return country

    def update(self, entity_id, entity_type, attribute, value):
        self.dm.update(entity_id, entity_type, attribute, value)
    
    def delete(self, entity_id, entity_type):
        self.dm.delete(entity_id, entity_type)

    def create_user(self, email, first_name, last_name, password):
        new_user = User(email, first_name, last_name, password)
        return new_user
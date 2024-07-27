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
    
    def update(self, entity_type, entity_id, attribute, value):
        action = file_handler(entity_type)
        if action == 5:
            print("There is no such type entity")
        else:
            data = self.get(entity_type)
            with open(action, "w") as filename:
                for datum in data:
                    if not entity_type =='Country' and datum["id"] == entity_id and attribute in datum:
                        datum[attribute] = value
                    elif entity_type == 'Country' and datum['code'] == entity_id and type(datum[attribute]) != list:
                        datum[attribute] = value
                    elif entity_type == 'Country' and datum['code'] == entity_id and type(datum[attribute]) == list:
                        datum[attribute].append(value)
                    
                json.dump(data, filename)
                    

    def delete(self, entity_type, entity_id):
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

    def update(self, entity_type, entity_id, attribute, value):
        self.dm.update(entity_type, entity_id, attribute, value)
    
    def delete(self, entity_type, entity_id):
        self.dm.delete(entity_type, entity_id)

    def create_user(self, email, first_name, last_name, password):
        new_user = User(email, first_name, last_name, password)
        return new_user
    
    def create_city(self, name, country_code):
        new_city = City(name, country_code)
        return new_city
    
    def create_amenity(self, name):
        new_amenity = Amenities(name)
        return new_amenity
    
    def create_place(self, name, description,
                 address, city_id,
                 latitude, longitude,
                 host_id, number_of_rooms,
                 bathrooms, price_per_night,
                 max_guests, amenities = None):
        new_place = Places(name, description,
                 address, city_id,
                 latitude, longitude,
                 host_id, number_of_rooms,
                 bathrooms, price_per_night,
                 max_guests, amenities = None)
        return new_place
    
    def create_review(self, user_id, place_id, comment, rating):
        new_review = Reviews(user_id, place_id, comment, rating)
        return new_review
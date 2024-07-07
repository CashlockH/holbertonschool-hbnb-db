import uuid
from datetime import date

class Places():
    places = []
    def __init__(self, name, description,
                 address, city_id,
                 latitude, longitude,
                 host_id, number_of_rooms,
                 bathrooms, price_per_night,
                 max_guests, amenities = None):
        
        self.id = uuid.uuid4()
        self.host_id = host_id
        self.name = name
        self.description = description
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.city_id = city_id
        self.amenity_ids = []

        if amenities is not None:
            self.amenity_ids = amenities

        self.reviews = []
        self.created_at = date.today()
    
    def add_review(self, user_id, feedback, rating):
        review = Reviews(user_id, self.id, feedback, rating)
        self.reviews.append(review)
        return review

    def to_dict(self):
        return {
            "type": "Place",
            "id": str(self.id),
            "host_id": str(self.host_id),
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "latitude": self.latitude,
            "longtitude": self.longitude,
            "number_of_rooms": self.number_of_rooms,
            "bathrooms": self.bathrooms,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "city_id": str(self.city_id),
            "amenity_ids": [str(amenity_id) for amenity_id in self.amenity_ids],
            "reviews": [review.to_dict() for review in self.reviews],
            "created_at": str(self.created_at)
        }

    

class User():
    def __init__(self,  email, password, first_name, last_name):
        self.id = uuid.uuid4()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.places = []
        self.created_at = date.today()
        self.updated_at = date.today()

    def create_place(self, name, description, address, city_id, latitude, longitude, number_of_rooms, bathrooms, price_per_night, max_guests, catalog, amenities = None,):

        for index, amenity in enumerate(amenities):
            amen_checker = 0
            for amen_name in catalog:
                if amen_name.name == amenity:
                    amenities[index] = amen_name
                    amen_checker = 1
            if amen_checker == 0:   
                new_amen = self.add_new_amenity(amenity)
                amenities[index] = new_amen

        
        new_place = Places(name, description, address, city_id, latitude, longitude, self.id, number_of_rooms, bathrooms, price_per_night, max_guests, amenities)
        self.places.append(new_place)
        Places.places.append(new_place)
        return new_place

    def add_new_amenity(self, name):
        new = Amenities(name)
        return new
    
    def write_review(self, place, feedback, rating):
        return place.add_review(self.id, feedback, rating)

    def to_dict(self):
        return {
            "type": "User",
            "id": str(self.id),
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "places": [place.to_dict() for place in self.places],
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }
    
    
class Reviews():
    def __init__(self, user_id, place_id, comment, rating):
        self.id = uuid.uuid4()
        self.created_at = date.today()
        self.updated_at = date.today()
        self.comment = comment
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    def to_dict(self):
        return {
            "type": "Review",
            "id": str(self.id),
            "user_id": str(self.user_id),
            "comment": self.comment,
            "rating":  self.rating,
            "place_id": str(self.place_id),
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }

class Amenities():
    def __init__(self, name):
        self.name = name
        self.id = uuid.uuid4()
        self.created_at = date.today()

    def to_dict(self):
        return {
            "type": "Amenity",
            "name": self.name,
            "id": self.id,
            "created_at": self.created_at
        }

    
class Country():
    countries = []
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.cities = []
        Country.countries.append(self)
    
    def new_city(self, name):
        new = City(name, self.code)
        self.cities.append(new.name)
        return new

    def to_dict(self):
        return {
            "type": "Country",
            "name": self.name,
            "code": self.code,
            "cities": self.cities
        }

class City():
    def __init__(self, name, country_code):
        self.name = name
        self.country_code = country_code
        self.id = uuid.uuid4()
    def to_dict(self):
        return {
            "type": "City",
            "name": self.name,
            "country": self.country_code,
            "id": str(self.id)
        }
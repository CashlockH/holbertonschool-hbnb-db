from flask import Flask, request
from persistency import PresentationLayer, DataManager
from datetime import date

app = Flask(__name__)

dm = DataManager()
presenter = PresentationLayer(dm)

@app.route("/users", methods=['POST', 'GET'])
@app.route("/users/<user_id>", methods=['GET', 'PUT', 'DELETE'])
def user(user_id=None):
    if request.method == 'POST':
        response = request.json
        email = response['email']
        first_name = response['first_name']
        last_name = response['last_name']
        password = response['password']
        user = presenter.create_user(email, first_name, last_name, password)
        presenter.save(user)
        if user:
            return {"msg": "User created"}, 201
    elif request.method == 'GET' and not user_id:
        response = presenter.get('User')
        return response, 200
    elif request.method == 'GET' and user_id:
        response = presenter.get('User', user_id)
        return response, 200
    elif request.method == 'DELETE':
        presenter.delete('User', user_id)
        return {"msg": 'User is deleted seccuessfully'}, 204
    elif request.method == 'PUT':
        response = request.json
        email = response['email']
        first_name = response['first_name']
        last_name = response['last_name']
        password = response['password']
        presenter.update('User', user_id, 'email', email)
        presenter.update('User', user_id, 'first_name', first_name)
        presenter.update('User', user_id, 'last_name', last_name)
        presenter.update('User', user_id, 'password', password)
        presenter.update('User', user_id, 'updated_at', date.today())
        presenter
        return {
            'msg': 'User is updated successfully'
        }, 200

@app.route('/countries', methods=['GET'])
@app.route('/countries/<country_code>')
@app.route('/countries/<country_code>/cities')
def country(country_code = None):
    if not country_code:
        country = presenter.get('Country')
        return country, 200
    elif not request.path.endswith('/cities'):
        country = presenter.get_country(country_code)
        return country, 200
    else:
        country = presenter.get_country(country_code)
        return {"Cities": country['cities']}, 200

@app.route('/cities', methods=['GET', 'POST'])
@app.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def city(city_id = None):
    if request.method == 'GET' and not city_id:
        city = presenter.get('City')
        return city, 200
    elif request.method == 'GET' and city_id:
        city = presenter.get('City', city_id)
        return city, 200
    elif request.method == 'POST':
        response = request.json
        city_name = response['name']
        country_code = response['country_code']
        city = presenter.create_city(city_name, country_code)
        presenter.save(city)
        presenter.update('Country', country_code, 'cities', city_name)
        return {"msg": 'City has been created successfully'}, 201
    elif request.method == 'PUT':
        response = request.json
        city_name = response['name']
        country_code = response['country_code']
        presenter.update('City', city_id, 'name', city_name)
        presenter.update('City', city_id, 'country_code', country_code)
        presenter.update('City', city_id, 'updated_at', date.today())
        return {'msg': 'City\'s information has been updated successfully'}, 200
    elif request.method == 'DELETE':
        presenter.delete('City', city_id)
        return {"msg": 'City has been deleted successfully'}, 204
    
@app.route('/amenities', methods=['GET', 'POST'])
@app.route('/amenities/<amenity_id>', methods = ['GET', 'PUT', 'DELETE'])
def amenities(amenity_id = None):
    if request.method == 'GET' and not amenity_id:
        response = presenter.get("Amenity")
        return response, 200
    elif request.method == 'POST':
        response = request.json
        amenity_name = request['name']
        amenity = presenter.create_amenity(amenity_name)
        presenter.save(amenity)
        return {'msg': 'New amenity has been created successfully'}, 201
    elif request.method == 'GET' and amenity_id:
        response = presenter.get("Amenity", amenity_id)
        return response, 200
    elif request.method == 'PUT':
        response = request.json
        amenity_name = request['name']
        presenter.update('Amenity', amenity_id, 'name', amenity_name)
        presenter.update('Amenity', amenity_id, 'updated_at', date.today())
        return {'msg': 'Amenity has been updated successfully'}, 200
    elif request.method == 'DELETE':
        presenter.delete('Amenity', amenity_id)
        return {'msg': 'Amenity has been deleted successfully'}, 204


@app.route('/places', methods = ['GET', 'POST'])
@app.route('/places/<place_id>', methods = ['GET', 'PUT', 'DELETE'])
def place(place_id = None):
    if request.method == 'POST':
        response = request.json
        name = response['name']
        description = response['description']
        address = response['address']
        city_id = response['city_id']
        latitude = response['latitude']
        longitude = response['longitude']
        host_id = response['host_id']
        number_of_rooms = response['number_of_rooms']
        number_of_bathrooms = response['number_of_bathrooms']
        price_per_night = response['price_per_night']
        max_guests = response['max_guests']
        amenity_ids = response['amenity_ids']
        place = presenter.create_place(name, description,
                 address, city_id,
                 latitude, longitude,
                 host_id, number_of_rooms,
                 number_of_bathrooms, price_per_night,
                 max_guests, amenity_ids)
        presenter.save(place)
        return {
            'msg': 'Place has been created successfully'
        }, 201
    if request.method == 'GET' and not place_id:
        response = presenter.get('Place')
        return response, 200
    elif request.method == 'GET' and place_id:
        response = presenter.get('Place', place_id)
        return response, 200
    elif request.method == 'PUT':
        response = request.json
        name = response['name']
        description = response['description']
        address = response['address']
        city_id = response['city_id']
        latitude = response['latitude']
        longitude = response['longitude']
        host_id = response['host_id']
        number_of_rooms = response['number_of_rooms']
        number_of_bathrooms = response['number_of_bathrooms']
        price_per_night = response['price_per_night']
        max_guests = response['max_guests']
        amenity_ids = response['amenity_ids']
        presenter.update('Place', place_id, 'name', name)
        presenter.update('Place', place_id, 'description', description)
        presenter.update('Place', place_id, 'address', address)
        presenter.update('Place', place_id, 'city_id', city_id)
        presenter.update('Place', place_id, 'latitude', latitude)
        presenter.update('Place', place_id, 'longitude', longitude)
        presenter.update('Place', place_id, 'host_id', host_id)
        presenter.update('Place', place_id, 'number_of_rooms', number_of_rooms)
        presenter.update('Place', place_id, 'number_of_bathrooms', number_of_bathrooms)
        presenter.update('Place', place_id, 'price_per_night', price_per_night)
        presenter.update('Place', place_id, 'max_guests', max_guests)
        presenter.update('Place', place_id, 'amenity_ids', amenity_ids)
        presenter.update('Place', place_id, 'updated_at', date.today())
        return {
            'msg': 'Place has been updated successfully'
        }, 200
    elif request.method == 'DELETE':
        presenter.delete('Place', place_id)
        return {
            'msg': 'Place has been deleted successfully'
        }, 204

@app.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def place_review(place_id):
    if request.method == 'POST':
        response = request.json
        user_id = response['user_id']
        comment = response['comment']
        rating = response['rating']
        place_review = presenter.create_review(user_id, place_id, comment, rating)
        presenter.save(place_review)
        presenter.update('Place', place_id, "reviews", place_review.id)
        return {
            'msg': 'Review has been created'
        }, 201
    elif request.method == 'GET':
        place = presenter.get("Place", place_id)
        reviews = []
        for review in place['reviews']:
            reviews.append(presenter.get("Review", review))
        return reviews, 200

@app.route('/users/<user_id>/reviews', methods=['GET'])
def retrive_user_reviews(user_id):
    user = presenter.get("User", user_id)
    reviews = []
    for review in user['reviews']:
        reviews.append(presenter.get("Review", review))
    return reviews, 200

@app.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def reviews(review_id):
    if request.method == 'GET':
        review = presenter.get('Review', review_id)
        return review, 200
    elif request.method == 'PUT':
        response = request.json
        user_id = response['user_id']
        comment = response['comment']
        rating = response['rating']
        place_id = response['id']
        presenter.update('Review', review_id, 'user_id', user_id)
        presenter.update('Review', review_id, 'comment', comment)
        presenter.update('Review', review_id, 'rating', rating)
        presenter.update('Review', review_id, 'place_id', place_id)
        presenter.update('Review', review_id, 'updated_at', date.today())
        return {
            'msg': 'Review has been updated successfully'
        }, 200
    elif request.method == 'DELETE':
        presenter.delete("Review", review_id)
        return {
            'msg': 'Review has been deleted successfully'
        }, 204
        



if __name__ == "__main__":
    app.run(debug=True)
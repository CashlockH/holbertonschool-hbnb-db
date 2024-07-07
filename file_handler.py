def file_handler(entity_type):
    actions = {
        'User': "user.json",
        'Place': "places.json",
        'Review': "reviews.json",
        'Amenity': "amenities.json",
        "City": "cities.json",
        "Country": "countries.json"
        }
    action = actions.get(entity_type, 5)
    return action
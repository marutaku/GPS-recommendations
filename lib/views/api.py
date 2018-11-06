from flask import Blueprint, g, request, jsonify
from lib.models.places import Place
from lib.models.Location import LocationModel

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('place', methods=['POST'])
def save_visited_place():
    place_model = Place()
    location_model = LocationModel()
    user_id = request.json['user_id']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    location_model.insert_location(user_id, latitude, longitude)
    place_model.detect_place(user_id)
    return jsonify(
        {'location': 'OK'}
    )

@api_bp.route('visited', methods=['POST'])
def post_visited_place():
    place_model = Place()
    user_id = request.json['user_id']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    arrivalDate = request.json['arraivalDate']
    departureDate = request.json['departureDate']
    print('====arrivalDate: {} ====='.format(arrivalDate))
    print('====departureDate: {} ====='.format(departureDate))
    print('Request catch.  user_id: {}'.format(user_id))
    place_model.insert_visited_place(user_id, latitude, longitude)
    return jsonify({
        'place': 'ok'
    })






    


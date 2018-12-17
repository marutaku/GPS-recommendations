from flask import Blueprint, g, request, jsonify
from lib.models.places import Place
from lib.models.Location import LocationModel
from lib.models.Monitoring import MonitoringModel
from datetime import datetime
from lib.models.Recommend import RecommendModel

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
    arrival_date_str = request.json['arraivalDate']
    departure_date_str = request.json['departureDate']
    arrival_date = datetime.strptime(arrival_date_str, '%Y-%m-%d %H:%M:%S')
    departure_date = datetime.strptime(departure_date_str, '%Y-%m-%d %H:%M:%S')
    print('====arrivalDate: {} ====='.format(arrival_date_str))
    print('====departureDate: {} ====='.format(departure_date_str))
    print('Request catch.  user_id: {}'.format(user_id))
    place_model.insert_visited_place(user_id, latitude, longitude, arrival_date, departure_date)
    return jsonify({
        'place': 'ok'
    })

@api_bp.route('recommend', methods=['POST'])
def get_recommendation():
    user_id = request.json['user_id']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    recommend = RecommendModel()
    result = recommend.get_recommend(user_id, latitude, longitude)
    return jsonify({
        'result': result
    })







    


from flask import Blueprint, g, request, jsonify
from lib.models.places import Place
from lib.models.Location import LocationModel

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('place', methods=['POST'])
def save_visited_place():
    place_model = Place()
    location_model = LocationModel()
    user_id = request.form['user_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    location_model.insert_location(user_id, latitude, longitude)
    place_model.detect_place(user_id)
    return jsonify(
        {'location': 'OK'}
    )



    


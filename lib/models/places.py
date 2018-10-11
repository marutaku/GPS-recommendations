from lib.database.VisitedPlace import VisitedPlaceDB
from lib.database.Location import LocationDB
from lib.database.Place import PlaceDB
from lib.util.geo import GEOUtil
from lib.models.Foursquare import Foursquare


class Place(object):

    def __init__(self):
        self.visited_db = VisitedPlaceDB()
        self.location_db = LocationDB()
        self.place_db = PlaceDB()
        self.foursquare = Foursquare()

    def detect_place(self, user_id):
        [current_location, prev_location] = self.location_db.get_location_history(user_id, limit=2)

        #     10分間で20m以上の移動がなければその場に滞在したと見なす(駅とかはまた考える)
        moving_distance = GEOUtil.cal_rho(
            current_location.latitude,
            current_location.longitude,
            prev_location.latitude,
            prev_location.longitude
        ) * 1000
        if moving_distance < 20:
            result_json = self.foursquare.search_place(
                current_location.latitude,
                current_location.longitude
            )
            place = result_json['response']['venues'][0]
            self.visited_db.insert_visited_place(user_id, place['id'])
            return
        else:
            return
    def fetch_place(self, latitude, longitude):
        result_json = self.foursquare.search_place(
                latitude,
                longitude
            )
        place = result_json['response']['venues'][0]
        return place

    def insert_visited_place(self, user_id, latitude, longitude):
        place_json = self.fetch_place(latitude, longitude)
        places = self.place_db.get_place_by_id(place_json['id'])
        if len(places) == 0:
            self.place_db.insert_place(place_json['name'], place_json['id'])
            place = self.place_db.get_place_by_id(place_json['id'])[0]
        else:
            place = places[0]
        self.visited_db.insert_visited_place(user_id, place.id)
        return


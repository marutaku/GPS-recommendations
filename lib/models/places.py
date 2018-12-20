from lib.database.VisitedPlace import VisitedPlaceDB
from lib.database.Location import LocationDB
from lib.database.Place import PlaceDB
from lib.database.Recommend import RecommendDB
from lib.models.UserModel import UserModel
from lib.models.Recommend import RecommendModel
from lib.database.User import UserDB
from lib.util.geo import GEOUtil
from lib.models.Foursquare import Foursquare
from lib.util.Slack import SlackUtil
import datetime, urllib

GOOGLE_MAP_BASE_URL = 'https://maps.google.co.jp/maps?q='


class Place(object):

    def __init__(self):
        self.visited_db = VisitedPlaceDB()
        self.location_db = LocationDB()
        self.place_db = PlaceDB()
        self.foursquare = Foursquare()
        self.user_model = UserModel()
        self.recommend = RecommendModel()
        self.user_db = UserDB()
        self.recommend_db = RecommendDB()

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

    def insert_visited_place(self, user_id, latitude, longitude, arrival_date, departure_date):
        user = self.user_db.get_user_by_id(user_id)
        place_json = self.fetch_place(latitude, longitude)
        print('=' * 30)
        print(place_json)
        print('=' * 30)
        places = self.place_db.get_place_by_id(place_json['id'])
        if len(places) == 0:
            self.place_db.insert_place(place_json['name'], place_json['id'], place_json['categories'][0]['shortName'])
            place = self.place_db.get_place_by_id(place_json['id'])[0]
        else:
            place = places[0]
        location_id = self.location_db.insert_location(user_id, latitude, longitude)
        self.visited_db.insert_visited_place(user_id, place.id, location_id, arrival_date, departure_date)
        now = datetime.datetime.now()
        if self.user_model.get_active_hour(user_id) <= now.hour and len(
                self.recommend.get_recommend_today(user_id)) == 0:
            # 推薦を行う
            recommend_place = self.recommend.get_recommend(user_id, latitude, longitude, location_id)
            place_name = list(recommend_place.keys())[0]
            recommend_latitude = list(recommend_place.values())[0]['latitude']
            recommend_longitude = list(recommend_place.values())[0]['longitude']
            url = '{url}{lat},{lng}'.format(
                url=GOOGLE_MAP_BASE_URL,
                lat=recommend_latitude,
                lng=recommend_longitude
            )
            text = '''日時: {date},
現在の緯度,経度: {lat}, {lng}, 
推薦された場所: {place}
GOOGLE MAPはこちら: {url}
アンケートはこちらから: {review}'''.format(
                date=datetime.datetime.now(),
                lat=latitude,
                lng=longitude,
                place=place_name,
                url=url,
                review='http://133.2.113.134/'
            )
            SlackUtil.post_slack(user.slack_id, text)

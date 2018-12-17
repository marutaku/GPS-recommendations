from lib.models.CollaborativeFiltering import CollaborativeFilter
from lib.models.Foursquare import Foursquare
from lib.models.places import Place
from lib.database.Recommend import RecommendDB
from lib.database.Location import LocationDB
from lib.database.Review import ReviewDB


class RecommendModel(object):
    def __init__(self):
        self.place_model = Place()
        self.fq = Foursquare()
        self.recommend_db = RecommendDB()
        self.location_db = LocationDB()
        self.review_db = ReviewDB()


    def get_recommend(self, user_id, latitude, longitude):
        cf = CollaborativeFilter(user_id)
        cf_recommend = cf.get_recommend(user_id, -1)
        cf_recommend_dict = {}
        for item in cf_recommend:
            key = list(item.keys())[0]
            value = list(item.values())[0]
            cf_recommend_dict[key] = value
        fq_recommend = self.fq.get_recommend_place(latitude, longitude)['response']['groups'][0]['items']
        fq_recommend_dict = {}

        for item in fq_recommend:
            item = item['venue']
            fq_recommend_dict[item['name']] = {
                'latitude': item['location']['lat'],
                'longitude': item['location']['lng']
            }

        # 各レコメンドの積集合を取得
        fq_place_name_set = set(fq_recommend_dict.keys())
        cf_place_name_set = set(cf_recommend_dict.keys())
        recommend_candidate = fq_place_name_set.intersection(cf_place_name_set)
        result_list = []
        for i in recommend_candidate:
            result_item = {i: cf_recommend_dict[i]}
            result_list.append(result_item)
        result_list.sort(key=lambda x: list(x.values())[0], reverse=True)
        recommend_item = result_list[0]
        recommend_place_name = list(recommend_item.keys())[0]
        place = self.place_model.get_place_by_name(recommend_place_name)[0]
        location_id = self.location_db.insert_location(user_id, latitude, longitude)
        self.recommend_db.insert_recommend_place(user_id, location_id, place.id)
        return recommend_item

    def get_recommend_history(self, user_id):
        return self.recommend_db.get_recommend_history(user_id)

    def get_recommend_by_id(self, id):
        return self.recommend_db.get_recommend_by_id(id)

    def insert_review(self, user_id, recommend_id, total_review, time_review, preference_review, distance_review):
        self.review_db.insert_review(user_id, recommend_id, total_review, time_review, preference_review,
                                     distance_review)
        self.recommend_db.update_review_status(recommend_id)


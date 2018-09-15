from lib.database.VisitedPlace import VisitedPlaceDB
from math import sqrt


class CollaborativeFilter(object):
    db = VisitedPlaceDB()

    def __init__(self, user_id):
        self.user_id = user_id

    def _get_visited_items(self):
        visited_places = self.db.get_visited_places(self.user_id)
        return self._create_place_dictionary(visited_places)

    def _get_others_visited_palce(self):
        others_visited_place = self.db.get_other_user_places(self.user_id)
        visited_dict_array = []
        for visited_place in others_visited_place:
            place_dict = self._create_place_dictionary(visited_place)
            visited_dict_array.append(place_dict)
        return visited_dict_array

    def _get_all_visited_places(self):
        visited_place = self.db.get_all_visited_place()
        return self._create_place_dictionary(visited_place)

    def _create_place_dictionary(self, visited_places):
        place_dict = {}
        for visited_place in visited_places:
            place_dict[visited_place.place.name] = visited_place.count
        return place_dict

    def get_similairty(self, person1_dict, person2_dict):

        ## 両者とも見た映画の集合を取る
        set_person1 = set(person1_dict.keys())
        set_person2 = set(person2_dict.keys())
        set_both = set_person1.intersection(set_person2)

        if len(set_both) == 0:  # 共通でみた映画がない場合は類似度を0とする
            return 0

        list_destance = []

        for item in set_both:
            # 同じ映画のレビュー点の差の2乗を計算
            # この数値が大きいほど「気が合わない」=「似ていない」と定義できる
            distance = pow(person1_dict[item] - person2_dict[item], 2)
            list_destance.append(distance)

        return 1 / (1 + sqrt(sum(list_destance)))  # 各映画の気の合わなさの合計の逆比的な指標を返す

    def get_recommend(self, person, top_N=10):

        totals = {}
        simSums = {}  # 推薦度スコアを入れるための箱を作っておく
        dataset = self._get_all_visited_places()

        # 自分以外のユーザのリストを取得してFor文を回す
        # # -> 各人との類似度、及び各人からの（まだ本人が見てない）映画の推薦スコアを計算するため
        # list_others = dataset.keys()
        # list_others.remove(person)
        list_others = self._get_others_visited_palce()

        for other in list_others:
            set_other = set(dataset[other])
            set_person = set(dataset[person])
            set_new_movie = set_other.difference(set_person)

            # あるユーザと本人の類似度を計算(simは0~1の数字)
            sim = self.get_similairty(person, other)

            # (本人がまだ見たことがない)映画のリストでFor分を回す
            for item in set_new_movie:
                # "類似度 x レビュー点数" を推薦度のスコアとして、全ユーザで積算する
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim

                # またユーザの類似度の積算値をとっておき、これで上記のスコアを除する
                simSums.setdefault(item, 0)
                simSums[item] += sim

        rankings = [(total / simSums[item], item) for item, total in totals.items()]
        rankings.sort()
        rankings.reverse()

        return [i[1] for i in rankings][:top_N]

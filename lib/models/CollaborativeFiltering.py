from lib.database.VisitedPlace import VisitedPlaceDB
from lib.database.Place import PlaceDB
from lib.database.User import UserDB
from math import sqrt


class CollaborativeFilter(object):

    def __init__(self, user_id):
        self.db = VisitedPlaceDB()
        self.user_db = UserDB()
        self.user_id = user_id
        self.place_db = PlaceDB()

    def _get_all_user_name(self):
        return self.user_db.get_all_user_name()

    def _get_all_visited_places(self):
        visited_place = self.db.get_group_visited_place()
        return self._create_user_dictionary(visited_place)

    def _create_user_dictionary(self, visited_places):
        place_dict = {}
        for visited_place in visited_places:
            user_name = self.user_db.get_user_by_id(visited_place.user_id).name
            place_name = self.place_db.get_place_by_db_id(visited_place.place_id).place_name
            if user_name not in place_dict:
                place_dict[user_name] = {}
            place_dict[user_name][place_name] = visited_place.count
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

    def get_recommend(self, user_id, top_N=10):

        totals = {}
        simSums = {}  # 推薦度スコアを入れるための箱を作っておく
        dataset = self._get_all_visited_places()

        # 自分以外のユーザのリストを取得してFor文を回す
        # # -> 各人との類似度、及び各人からの（まだ本人が見てない）映画の推薦スコアを計算するため
        # list_others = dataset.keys()
        # list_others.remove(person)
        list_others = list(map(lambda user: user.name,self._get_all_user_name()))
        user_name = self.user_db.get_user_by_id(user_id).name

        for other in list_others:
            set_other = set(dataset[other])
            set_person = set(dataset[user_name])
            set_new_place = set_other.difference(set_person)

            # あるユーザと本人の類似度を計算(simは0~1の数字)
            sim = self.get_similairty(dataset[user_name], dataset[other])

            # (本人がまだ見たことがない)映画のリストでFor分を回す
            for item in set_new_place:
                # "類似度 x レビュー点数" を推薦度のスコアとして、全ユーザで積算する
                totals.setdefault(item, 0)
                totals[item] += dataset[other][item] * sim

                # またユーザの類似度の積算値をとっておき、これで上記のスコアを除する
                simSums.setdefault(item, 0)
                simSums[item] += sim

        rankings = []
        for item, total in totals.items():
            if simSums[item] != 0:
                rankings.append((total / simSums[item], item))
        rankings.sort()
        rankings.reverse()

        return [{i[1]: i[0]} for i in rankings][:top_N]

if __name__ == '__main__':
    cf = CollaborativeFilter(1)
    print(cf._get_all_visited_places())


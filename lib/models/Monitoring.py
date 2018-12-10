from lib.database.VisitedPlace import VisitedPlaceDB
from lib.database.User import UserDB

class MonitoringModel():
    def __init__(self):
        self.visited_place = VisitedPlaceDB()
        self.user_db = UserDB()

    def check_dead_user(self, start_date, end_date):
        survive_user = self.visited_place.get_today_activity(start_date, end_date)
        all_user = self.user_db.get_all_user()
        survive_user_set = set([user.user_id for user in survive_user])
        all_user_set = set([user.id for user in all_user])
        print('All user: {}'.format(all_user_set))
        print('Survive user: {}'.format(survive_user_set))
        return all_user_set - survive_user_set



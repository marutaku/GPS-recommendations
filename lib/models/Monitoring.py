from lib.database.Monitoring import MonitoringDB
from lib.database.User import UserDB

class MonitoringModel():
    def __init__(self):
        self.monitoring_db = MonitoringDB()
        self.user_db = UserDB()

    def insert_monitoring(self, user_id):
        self.monitoring_db.insert_state(user_id)

    def check_dead_user(self, start_date, end_date):
        survive_user = self.monitoring_db.get_survive_user(start_date, end_date)
        all_user = self.user_db.get_all_user()
        survive_user_set = set([user.user_id for user in survive_user])
        all_user_set = set([user.id for user in all_user])
        print('All user: {}'.format(all_user_set))
        print('Survive user: {}'.format(survive_user_set))
        return all_user_set - survive_user_set



from lib.database.User import UserDB
from lib.database.VisitedPlace import VisitedPlaceDB
import hashlib

class UserModel(object):
    def __init__(self):
        self.user_db = UserDB()
        self.visited_db = VisitedPlaceDB()

    def login(self, name, password):
        hashed_passoword = self.hash_password(password)
        user = self.user_db.get_user_by_name(name)
        if len(user) != 0 and user[0].password == hashed_passoword:
            return user[0]
        else:
            return None

    def create_user(self, username, password):
        hashed_password = self.hash_password(password)
        is_user = self.user_db.get_user_by_name(username)
        if len(password) <= 6:
            raise Exception('パスワードが短すぎます')
        elif len(is_user) == 0:
            self.user_db.create_user(username, hashed_password)
            return True
        elif is_user != 0:
            raise Exception('ユーザ名はすでに存在しています')
    def update_password(self, username, password):
        hashed_password = self.hash_password(password)
        self.user_db.update_password(username, hashed_password)


    def hash_password(self, password):
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        return md5.hexdigest()

    def get_all_visited_place(self, user_id):
        visited_places = self.visited_db.get_visited_places(user_id)
        return visited_places

    def get_active_hour(self, user_id):
        return self.user_db.get_user_by_id(user_id).active_hour

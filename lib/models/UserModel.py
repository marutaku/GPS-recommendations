from lib.database.User import UserDB
import hashlib

class UserModel(object):
    def __init__(self):
        self.user_db = UserDB()

    def login(self, name, password):
        hashed_passoword = self.hash_password(password)
        user = self.user_db.get_user_by_name(name)[0]
        if (user.password == hashed_passoword):
            return user
        else:
            return False

    def create_user(self, username, password):
        hashed_password = self.hash_password(password)
        if len(self.user_db.get_user_by_name(username)) == 0:
            self.user_db.create_user(username, hashed_password)
            return True
        else:
            return False

    def hash_password(self, password):
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        return md5.hexdigest()

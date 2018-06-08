from lib import db

class AbstractModel:
    def __init__(self, db):
        self.db = db
    def rollback(self):
        self.db.session.rollback()
    def commit(self):
        self.db.session.commit()
    @classmethod
    def init(self):
        self.db.create_all()


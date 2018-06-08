from lib.core import db

class VisitedPlace(db.Model):
    __tablename__ = 'visited_place'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id', onupdate='CASCADE', ondelete='CASCADE'))
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class VisitedPlaceDB(object):
    def insert_visited_place(self, user_id, place_id):
        visited_place = VisitedPlace(user_id = user_id, place_id = place_id)
        db.session.add(visited_place)
        db.session.commit()

    @staticmethod
    def init():
        db.create_all()

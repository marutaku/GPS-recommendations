from lib.core import db
from sqlalchemy import func
from sqlalchemy.orm import relationship


class VisitedPlace(db.Model):
    __tablename__ = 'visited_place'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id', onupdate='CASCADE', ondelete='CASCADE'))
    arrival_date = db.Column(db.DateTime, nullable=False)
    departure_date = db.Column(db.DateTime, nullable=False)
    visited_time = db.Column(db.Time, nullable=False)
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    place = relationship('Place')
    user = relationship('User')


class VisitedPlaceDB(object):
    def insert_visited_place(self, user_id, place_id, arrival_date, departure_date):
        visited_time = departure_date - arrival_date
        visited_place = VisitedPlace(
            user_id=user_id,
            place_id=place_id,
            arrival_date=arrival_date,
            departure_date=departure_date,
            visited_time=visited_time
        )
        db.session.add(visited_place)
        db.session.commit()

    def get_visited_places(self, user_id):
        visited_place = db.session.query(VisitedPlace, func.count(VisitedPlace.place_id)) \
            .filter(VisitedPlace.user_id == user_id).all()
        return visited_place

    def get_other_user_places(self, user_id):
        visited_place = db.session.query(VisitedPlace, func.count(VisitedPlace.place_id)) \
            .filter(VisitedPlace.user_id != user_id).all()
        return visited_place

    def get_all_visited_place(self):
        visited_place = db.session.query(VisitedPlace).all()

        return visited_place

    @staticmethod
    def init():
        db.create_all()

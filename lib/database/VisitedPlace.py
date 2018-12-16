from lib.core import db
from sqlalchemy import func
from sqlalchemy.orm import relationship
import datetime

MISS_DEPARTURE_VALUE = datetime.datetime.strptime('4001-01-01 09:00:00', '%Y-%m-%d %H:%M:%S')


class VisitedPlace(db.Model):
    __tablename__ = 'visited_place'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    place_id = db.Column(db.Integer, db.ForeignKey('place.id', onupdate='CASCADE', ondelete='CASCADE'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', onupdate='CASCADE', ondelete='CASCADE'),
                            nullable=True)
    arrival_date = db.Column(db.DateTime, nullable=True)
    departure_date = db.Column(db.DateTime, nullable=True)
    visited_time = db.Column(db.Time, nullable=True)
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    place = relationship('Place')
    user = relationship('User')
    location = relationship('Location')


class VisitedPlaceDB(object):
    def insert_visited_place(self, user_id, place_id, location_id, arrival_date, departure_date):
        visited_time = departure_date - arrival_date
        if departure_date == MISS_DEPARTURE_VALUE:
            visited_place = VisitedPlace(
                user_id=user_id,
                place_id=place_id,
                location_id=location_id,
                arrival_date=arrival_date,
                departure_date=None,
                visited_time=None
            )
        else:
            visited_place = VisitedPlace(
                user_id=user_id,
                place_id=place_id,
                arrival_date=arrival_date,
                departure_date=departure_date,
                visited_time=visited_time
            )
        db.session.add(visited_place)
        db.session.commit()

    def get_visited_places_count(self, user_id):
        visited_place = db.session.query(VisitedPlace, func.count(VisitedPlace.place_id)) \
            .filter(VisitedPlace.user_id == user_id).all()
        return visited_place

    def get_visited_places(self, user_id):
        visited_place = db.session.query(VisitedPlace) \
            .filter(VisitedPlace.user_id == user_id).order_by(VisitedPlace.create_at.desc()).all()
        return visited_place

    def get_other_user_places(self, user_id):
        visited_place = db.session.query(VisitedPlace, func.count(VisitedPlace.place_id)) \
            .filter(VisitedPlace.user_id != user_id).all()
        return visited_place

    def get_group_visited_place(self, hours=8):
        visited_place = db.session.query(
            VisitedPlace.user_id,
            func.count(VisitedPlace.place_id).label('count'),
            VisitedPlace.place_id,
        ).filter(
            # 常在地を除外
            VisitedPlace.visited_time <= datetime.timedelta(hours=hours)
        ).group_by(VisitedPlace.user_id, VisitedPlace.place_id).all()

        return visited_place

    def get_today_activity(self, start_date, end_date):
        survive_user = db.session.query(VisitedPlace) \
            .filter(VisitedPlace.create_at.between(start_date, end_date)).all()
        return survive_user

    @staticmethod
    def init():
        db.create_all()

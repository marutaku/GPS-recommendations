from lib.core import db
from sqlalchemy import func, desc
from sqlalchemy.orm import relationship


class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    user = relationship('User')


class LocationDB(object):
    def insert_location(self, user_id, latitude, longitude):
        location = Location(user_id=user_id, latitude=latitude, longitude=longitude)
        db.session.add(location)
        db.session.commit()

    def get_location_history(self, user_id, limit=5):
        locations = db.session.query(Location).filter(Location.user_id==user_id)\
            .order_by(desc(Location.create_at)).limit(limit).all()
        return locations

    @staticmethod
    def init():
        db.create_all()

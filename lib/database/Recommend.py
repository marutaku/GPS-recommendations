from lib.core import db
from sqlalchemy import func
from sqlalchemy.orm import relationship

class Recommend(db.Model):
    __tablename__ = 'recommend'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    location_id = db.Column(db.ForeignKey('locations.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True)
    place_id = db.Column(db.ForeignKey('place.id', onupdate='CASCADE', ondelete='CASCADE'))
    is_reviewed = db.Column(db.Boolean, default=False)
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    place = relationship('Place')
    user = relationship('User')
    location = relationship('Location')

class RecommendDB(object):
    def insert_recommend_place(self, user_id, location_id, place_id):
        new_recommend = Recommend(
            user_id=user_id,
            location_id=location_id,
            place_id=place_id
        )
        db.session.add(new_recommend)
        db.session.commit()

    def get_recommend_history(self, user_id):
        return db.session.query(Recommend)\
            .filter(Recommend.user_id == user_id)\
            .all()

    def get_recommend_by_id(self, recommend_id):
        return db.session.query(Recommend).get(recommend_id)

    def update_review_status(self, id, status=True):
        target = db.session.query(Recommend).get(id)
        target.is_reviewed = status
        db.session.commit()

    def get_recommend_between(self, user_id, start_date, end_date):
        return db.session.query(Recommend)\
            .filter(Recommend.create_at <= end_date)\
            .filter(Recommend.create_at > start_date)\
            .filter(Recommend.user_id == user_id).all()

    @staticmethod
    def init():
        db.create_all()

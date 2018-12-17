from lib.core import db
from sqlalchemy import func
from sqlalchemy.orm import relationship
import datetime

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    recommend_id = db.Column(db.Integer, db.ForeignKey('recommend.id', onupdate='CASCADE', ondelete='CASCADE'))
    total_review = db.Column(db.Integer)
    time_review = db.Column(db.Integer)
    preference_review = db.Column(db.Integer)
    distance_review = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    user = relationship('User')
    recommend = relationship('Recommend')


class ReviewDB(object):
    def insert_review(self, user_id, recommend_id, total_review, time_review, preference_review, distance_review):
        new_review = Review(
            user_id=user_id,
            recommend_id=recommend_id,
            total_review=total_review,
            time_review=time_review,
            preference_review=preference_review,
            distance_review=distance_review
        )
        db.session.add(new_review)
        db.session.commit()

    @staticmethod
    def init():
        db.create_all()

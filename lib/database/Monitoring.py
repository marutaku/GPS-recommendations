from lib.core import db
from sqlalchemy import func
from sqlalchemy.orm import relationship

class Monitoring(db.Model):
    __tablename__ = 'monitoring'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    user = relationship('User')


class MonitoringDB(object):
    def insert_state(self, user_id):
        state = Monitoring(
            user_id=user_id
        )
        db.session.add(state)
        db.session.commit()

    def get_survive_user(self, start_date, end_date):
        survive_user = db.session.query(Monitoring)\
            .filter(Monitoring.create_at > start_date)\
            .filter(Monitoring.create_at < end_date).all()
        return survive_user

    @staticmethod
    def init():
        db.create_all()


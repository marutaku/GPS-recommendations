from lib.core import db

class Place(db.Model):
    id = db.Column(db.String, primary_key=True, autoincrement=True)
    place_name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(256), nullable=True, server_default='')
    create_at = db.Column(db.TIMESTAMP, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


class PlaceDB(object):
    def check_place(self, place_name):
        return len(db.session.query(Place).filter(Place.place_name == place_name).all()) != 0

    def get_place_id(self, place_name):
        return db.session.query(Place).filter(Place.place_name == place_name).all()

    def insert_place(self, place_name, description = ''):
        place = Place(place_name = place_name, description = description)
        db.session.add(place)
        db.session.commit()

    @staticmethod
    def init():
        db.create_all()

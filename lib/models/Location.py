from lib.database.Location import LocationDB

class LocationModel(object):
    def __init__(self):
        self.location_db = LocationDB()

    def insert_location(self, user_id, latitude, longitude):
        self.location_db.insert_location(user_id, latitude, longitude)

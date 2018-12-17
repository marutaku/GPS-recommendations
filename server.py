from flask_script import Manager, Server, prompt_bool
from lib import app
from lib.database.User import UserDB
from lib.database.Place import PlaceDB
from lib.database.Location import LocationDB
from lib.database.Monitoring import MonitoringDB
from lib.database.Recommend import RecommendDB
from lib.database.Review import ReviewDB
from lib.database.VisitedPlace import VisitedPlaceDB

manager = Manager(app)

@manager.command
def init_db():
    for Db in [UserDB, PlaceDB, VisitedPlaceDB, LocationDB, MonitoringDB, ReviewDB, RecommendDB]:
        Db.init()

if __name__ == '__main__':
    manager.run()


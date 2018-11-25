from lib import factory
from lib.core import db

app = factory.create_app(__name__)

from lib import controller


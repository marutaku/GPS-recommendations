# Initialize all modules
from flask import Flask
from lib import views
from lib.core import db
from logging.config import dictConfig

def create_app(package_name):
    app = Flask(package_name, template_folder = '../template')
    app.config.from_object('lib.config')
    db.init_app(app)
    views.init_app(app)
    return app


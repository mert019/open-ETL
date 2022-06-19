import logging

from flask import Flask
from flask_appbuilder import AppBuilder

from database import init_db


"""Logging configuration"""
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)


app = Flask(__name__)
app.config.from_object("config")


init_db(app)

from database import db

from .index import AppIndexView
appbuilder = AppBuilder(app, db.session, indexview=AppIndexView)


from . import views
from . import apis

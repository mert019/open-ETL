from flask import Flask
from flask_appbuilder import SQLA


db : SQLA = None


def init_db(app : Flask) -> None:
    global db
    """Initializes database object."""
    db = SQLA(app)

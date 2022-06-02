from enum import Enum
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


class DatabaseEngine(Model):
    id = Column(Integer, primary_key=True)
    engine_name = Column(String(64), unique = True, nullable=False)

    def __repr__(self):
        return self.engine_name


class DatabaseEngineEnum(Enum):
    POSTGRESQL = 1
    MSSQLSERVER = 2

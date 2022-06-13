from enum import Enum
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


class LoadType(Model):
    id = Column(Integer, primary_key=True)
    load_type = Column(String(64), unique = True, nullable=False)

    def __repr__(self):
        return self.load_type


class LoadTypeEnum(Enum):
    TO_DATABASE = 1

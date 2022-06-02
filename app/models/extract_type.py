from enum import Enum
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


class ExtractType(Model):
    id = Column(Integer, primary_key=True)
    extract_type = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.extract_type


class ExtractTypeEnum(Enum):
    FROM_DATABASE = 1
    FROM_EXCEL = 2
    FROM_CSV = 3

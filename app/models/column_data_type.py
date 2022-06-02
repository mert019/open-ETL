from enum import Enum
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String



class ColumnDataType(Model):
    id = Column(Integer, primary_key=True)
    data_type = Column(String(64), unique = True, nullable=False)

    def __repr__(self):
        return self.data_type


class ColumnDataTypeEnum(Enum):
    INT = 1
    FLOAT = 2
    STR = 3
    BOOL = 4
    DATETIME = 5

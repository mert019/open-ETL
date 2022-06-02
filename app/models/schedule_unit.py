from enum import Enum
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


class ScheduleUnit(Model):
    id = Column(Integer, primary_key=True)
    unit_name = Column(String(64), unique=True, nullable=False)

    def __repr__(self):
        return self.unit_name


class ScheduleUnitEnum(Enum):
    MINUTE = 1
    HOUR = 2
    DAY = 3

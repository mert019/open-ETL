from enum import Enum
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


class OperationLogType(Model):
    id = Column(Integer, primary_key=True)
    log_type = Column(String(32), unique=True, nullable=False)

    def __repr__(self):
        return self.log_type


class OperationLogTypeEnum(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

from enum import Enum
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String


class FTPType(Model):
    id = Column(Integer, primary_key=True)
    type_name = Column(String(64), unique = True, nullable=False)

    def __repr__(self):
        return self.type_name


class FTPTypeEnum(Enum):
    FTP = 1
    SFTP = 2

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.models.load_type import LoadType


class LoadTarget(Model):
    id = Column(Integer, primary_key=True)
    load_target_name = Column(String(64), unique=True, nullable=False)
    load_type_id = Column(Integer, ForeignKey('load_type.id'), nullable=False)

    load_type = relationship('LoadType')

    def __repr__(self):
        return self.load_target_name

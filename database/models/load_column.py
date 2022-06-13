from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.models.load_target import LoadTarget


class LoadColumn(Model):
    id = Column(Integer, primary_key=True)
    column_name = Column(String(64), nullable=False)
    is_makes_record_unique = Column(Boolean, default=False)
    column_data_type_id = Column(Integer, ForeignKey('column_data_type.id'), nullable=False)
    load_target_id = Column(Integer, ForeignKey('load_target.id'), nullable=False)
    
    column_data_type = relationship('ColumnDataType')
    load_target = relationship('LoadTarget')

    def __repr__(self):
        return f"{self.load_target.load_target_name} - {self.column_name}"

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.models.column_data_type import ColumnDataType
from database.models.extract_source import ExtractSource


class ExtractColumn(Model):
    id = Column(Integer, primary_key=True)
    column_name = Column(String(64), nullable=False)
    column_index = Column(Integer, nullable=True)
    column_data_type_id = Column(Integer, ForeignKey('column_data_type.id'), nullable=False)
    extract_source_id = Column(Integer, ForeignKey('extract_source.id'), nullable=False)
    
    column_data_type = relationship('ColumnDataType')
    extract_source = relationship('ExtractSource')

    def __repr__(self):
        return f"{self.extract_source.extract_source_name} - {self.column_name}"

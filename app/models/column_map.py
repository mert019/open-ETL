from flask_appbuilder import Model
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.operation_config import OperationConfig
from app.models.extract_column import ExtractColumn
from app.models.load_column import LoadColumn


class ColumnMap(Model):
    id = Column(Integer, primary_key=True)
    extract_column_id = Column(Integer, ForeignKey('extract_column.id'), nullable=False)
    load_column_id = Column(Integer, ForeignKey('load_column.id'), nullable=False)
    operation_config_id = Column(Integer, ForeignKey('operation_config.id'), nullable=False)
    
    extract_column = relationship('ExtractColumn', foreign_keys=[extract_column_id])
    load_column = relationship('LoadColumn', foreign_keys=[load_column_id])
    operation_config = relationship('OperationConfig', foreign_keys=[operation_config_id])

    #TODO: Transform config.


    def __repr__(self):
        return f"{self.extract_column.column_name}"

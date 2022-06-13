from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database.models.operation_history import OperationHistory


class ExtractFile(Model):
    id = Column(Integer, primary_key=True)
    source_name = Column(String(128), nullable=False)
    unique_name = Column(String(128), unique=True, nullable=False)
    extension = Column(String(16))
    process_again = Column(Boolean, default=False, nullable=False)
    operation_history_id = Column(Integer, ForeignKey('operation_history.id'), nullable=False)

    operation_history = relationship('OperationHistory', foreign_keys=[operation_history_id])
    
    def __repr__(self):
        return f"{self.operation_history_id} - {self.source_name}"

    @staticmethod
    def create(db, source_name, unique_name, extension, operation_history_id):
        obj = ExtractFile(
            source_name=source_name,
            unique_name=unique_name,
            extension=extension,
            operation_history_id=operation_history_id
        )
        db.session.add(obj)
        db.session.commit()

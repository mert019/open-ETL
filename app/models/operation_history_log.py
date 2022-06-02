import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.models.operation_log_type import OperationLogType
from app.models.operation_history import OperationHistory


class OperationHistoryLog(Model):
    id = Column(Integer, primary_key=True)
    log_date_time = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    log_message = Column(String(2048))
    operation_log_type_id = Column(Integer, ForeignKey('operation_log_type.id'), nullable=False)
    operation_history_id = Column(Integer, ForeignKey('operation_history.id'), nullable=False)

    operation_log_type = relationship('OperationLogType', foreign_keys=[operation_log_type_id])
    operation_history = relationship('OperationHistory', foreign_keys=[operation_history_id])
    

    def __repr__(self):
        return f"{self.id} - {self.operation_log_type}"

    @staticmethod
    def create(db, operation_history_id, msg, operation_log_type_id):
        obj = OperationHistoryLog(
            operation_history_id=operation_history_id, 
            log_message=msg, 
            operation_log_type_id=operation_log_type_id
        )
        db.session.add(obj)
        db.session.commit()

import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from database.models.operation_config import OperationConfig

class OperationHistory(Model):
    id = Column(Integer, primary_key=True)
    start_date_time = Column(DateTime, default=datetime.datetime.now, nullable=False)
    end_date_time = Column(DateTime)
    is_successfully_ended = Column(Boolean, default=False)
    records_extracted = Column(Integer, default=0)
    records_loaded = Column(Integer, default=0)
    operation_config_id = Column(Integer, ForeignKey('operation_config.id'), nullable=False)

    operation_config = relationship('OperationConfig', foreign_keys=[operation_config_id])

    
    def __repr__(self):
        return f"{self.id}"


    @staticmethod
    def create(db, operation_config_id):
        """
            Creates a OperationHistory record with the given operation config id.
            Returns the created record.
        """
        obj = OperationHistory(operation_config_id=operation_config_id)
        db.session.add(obj)
        db.session.commit()
        return obj
        

    @staticmethod
    def get_last_success(db, operation_config_id):
        """Returns the latest successful execution for given operation_config_id."""
        obj = db.session.query(OperationHistory).filter(
            (OperationHistory.operation_config_id == operation_config_id)
            & (OperationHistory.is_successfully_ended == True)).order_by(OperationHistory.start_date_time.desc()).first()
        return obj


    @staticmethod
    def get_last_failure(db, operation_config_id):
        """Returns the latest failed execution for given operation_config_id."""
        obj = db.session.query(OperationHistory).filter(
            (OperationHistory.operation_config_id == operation_config_id)
            & (OperationHistory.is_successfully_ended == False)
            & (OperationHistory.end_date_time != None)).order_by(OperationHistory.start_date_time.desc()).first()
        return obj

    @staticmethod
    def get_last(db, operation_config_id):
        """Returns the latest  execution for given operation_config_id."""
        obj = db.session.query(OperationHistory).filter(
            (OperationHistory.operation_config_id == operation_config_id)
            & (OperationHistory.end_date_time != None)).order_by(OperationHistory.start_date_time.desc()).first()
        return obj

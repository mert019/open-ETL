from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.models.schedule_unit import ScheduleUnit


class OperationConfig(Model):
    id = Column(Integer, primary_key=True)
    operation_name = Column(String(64), unique = True, nullable=False)
    description = Column(String(128), nullable=False)
    is_in_process = Column(Boolean, default=False)
    is_schedule_enabled = Column(Boolean, default=False)
    schedule_interval = Column(Integer, nullable=False)
    transform_query = Column(String(4096), nullable=False)
    show_on_dashboard = Column(Boolean, default=False)
    extract_source_id = Column(Integer, ForeignKey('extract_source.id'), nullable=False)
    load_target_id = Column(Integer, ForeignKey('load_target.id'), nullable=False)
    schedule_unit_id = Column(Integer, ForeignKey('schedule_unit.id'), nullable=False)

    extract_source = relationship('ExtractSource')
    load_target = relationship('LoadTarget')
    schedule_unit = relationship('ScheduleUnit')
    
    def __repr__(self):
        return f"{self.operation_name}"


    @staticmethod
    def get_all_enabled(db):
        """Returns all enabled OperationConfigs"""
        return db.session.query(OperationConfig).filter((OperationConfig.is_schedule_enabled)).all()


    @staticmethod
    def set_all_is_in_process_to_false(db):
        """Sets is_in_process to false for all OperationConfig records."""
        operation_configs = db.session.query(OperationConfig).all()
        for obj in operation_configs:
            obj.is_in_process = False
        db.session.commit()        

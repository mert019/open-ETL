from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.models.database_connection import DatabaseConnection


class DatabaseLoadConfig(Model):
    id = Column(Integer, primary_key=True)
    table_name = Column(String(1024), nullable=False)
    delete_all_before_load = Column(Boolean, default=False)
    insert_record = Column(Boolean, default=True)
    update_record = Column(Boolean, default=False)
    start_transaction = Column(Boolean, default=False)
    load_target_id = Column(Integer, ForeignKey('load_target.id'), nullable=False, unique=True)
    database_connection_id = Column(Integer, ForeignKey('database_connection.id'), nullable=False)

    load_target = relationship('LoadTarget', foreign_keys=[load_target_id])
    database_connection = relationship('DatabaseConnection', foreign_keys=[database_connection_id])

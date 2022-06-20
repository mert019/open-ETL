from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.models.database_engine import DatabaseEngine


class DatabaseConnection(Model):
    id = Column(Integer, primary_key=True)
    conn_name = Column(String(128), unique=True, nullable=False)
    conn_db_hostname = Column(String(1024), unique=False, nullable=False)
    conn_db_port = Column(Integer, unique=False, nullable=False)
    conn_db_username = Column(String(1024), unique=False, nullable=False)
    conn_db_password = Column(String(1024), unique=False, nullable=False)
    conn_db_name = Column(String(1024), unique=False, nullable=False)
    database_engine_id = Column(Integer, ForeignKey('database_engine.id'), nullable=False)

    database_engine = relationship('DatabaseEngine', foreign_keys=[database_engine_id])


    def __repr__(self):
        return f"{self.conn_name}"

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.models import ExtractSource


class DatabaseExtractConfig(Model):
    id = Column(Integer, primary_key=True)
    query = Column(String(1024), unique=False, nullable=False)
    conn_db_hostname = Column(String(1024), unique=False, nullable=False)
    conn_db_port = Column(Integer, unique=False, nullable=False)
    conn_db_username = Column(String(1024), unique=False, nullable=False)
    conn_db_password = Column(String(1024), unique=False, nullable=False)
    conn_db_name = Column(String(1024), unique=False, nullable=False)
    query = Column(String(1024), unique=False, nullable=False)
    extract_source_id = Column(Integer, ForeignKey('extract_source.id'), unique=True, nullable=False)
    database_engine_id = Column(Integer, ForeignKey('database_engine.id'), nullable=False)

    extract_source = relationship('ExtractSource', foreign_keys=[extract_source_id])
    database_engine = relationship('DatabaseEngine', foreign_keys=[database_engine_id])

    def __repr__(self):
        return f"{self.conn_db_hostname} - {self.conn_db_port} - {self.conn_db_name} - {self.conn_db_username}"

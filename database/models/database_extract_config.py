from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.models.database_connection import DatabaseConnection


class DatabaseExtractConfig(Model):
    id = Column(Integer, primary_key=True)
    query = Column(String(1024), unique=False, nullable=False)
    extract_source_id = Column(Integer, ForeignKey('extract_source.id'), unique=True, nullable=False)
    database_connection_id = Column(Integer, ForeignKey('database_connection.id'), nullable=False)

    extract_source = relationship('ExtractSource', foreign_keys=[extract_source_id])
    database_connection = relationship('DatabaseConnection', foreign_keys=[database_connection_id])

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.models.ftp_connection import FtpConnection


class ExcelExtractConfig(Model):
    id = Column(Integer, primary_key=True)
    extract_directory = Column(String(512), unique=False, nullable=True)
    read_file_name = Column(String(512), nullable=True)
    read_file_name_regex = Column(String(512), nullable=True)
    table_start_index = Column(Integer, nullable=True)
    ignore_last_n_rows = Column(Integer, nullable=True)
    has_headers = Column(Boolean, nullable=True, default=True)
    extract_source_id = Column(Integer, ForeignKey('extract_source.id'), unique=True, nullable=False)
    ftp_connection_id = Column(Integer, ForeignKey('ftp_connection.id'), unique=False, nullable=False)

    extract_source = relationship('ExtractSource', foreign_keys=[extract_source_id])
    ftp_connection = relationship('FtpConnection', foreign_keys=[ftp_connection_id])

    def __repr__(self):
        return f"Excel from {self.ftp_connection.ftp_hostname}"

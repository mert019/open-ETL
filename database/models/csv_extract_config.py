from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


from database.models.ftp_type import FTPType


class CSVExtractConfig(Model):
    id = Column(Integer, primary_key=True)
    ftp_hostname = Column(String(256), nullable=False)
    ftp_port = Column(Integer, nullable=False)
    ftp_username = Column(String(256), nullable=False)
    ftp_password = Column(String(256), nullable=False)
    extract_directory = Column(String(512), unique=False, nullable=True)
    seperator = Column(String(8), nullable=True)
    read_file_name = Column(String(512), nullable=True)
    read_file_name_regex = Column(String(512), nullable=True)
    table_start_index = Column(Integer, nullable=True)
    ignore_last_n_rows = Column(Integer, nullable=True)
    has_headers = Column(Boolean, nullable=True, default=True)
    extract_source_id = Column(Integer, ForeignKey('extract_source.id'), unique=True, nullable=False)
    ftp_type_id = Column(Integer, ForeignKey('ftp_type.id'), nullable=False)

    extract_source = relationship('ExtractSource', foreign_keys=[extract_source_id])
    ftp_type = relationship('FTPType', foreign_keys=[ftp_type_id])

    def __repr__(self):
        return f"CSV from {self.ftp_hostname}"

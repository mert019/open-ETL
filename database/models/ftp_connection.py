from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.models.ftp_type import FTPType


class FtpConnection(Model):
    id = Column(Integer, primary_key=True)
    conn_name = Column(String(128), unique=True, nullable=False)
    ftp_hostname = Column(String(256), nullable=False)
    ftp_port = Column(Integer, nullable=False)
    ftp_username = Column(String(256), nullable=False)
    ftp_password = Column(String(256), nullable=False)
    ftp_type_id = Column(Integer, ForeignKey('ftp_type.id'), nullable=False)

    ftp_type = relationship('FTPType', foreign_keys=[ftp_type_id])


    def __repr__(self):
        return f"{self.conn_name}"

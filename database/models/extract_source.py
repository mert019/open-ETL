from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ExtractSource(Model):
    id = Column(Integer, primary_key=True)
    extract_source_name = Column(String(64), unique=True, nullable=False)
    extract_type_id = Column(Integer, ForeignKey('extract_type.id'), nullable=False)
    
    extract_type = relationship('ExtractType')

    def __repr__(self):
        return self.extract_source_name

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class DatabaseLoadConfig(Model):
    id = Column(Integer, primary_key=True)
    
    table_name = Column(String(1024), nullable=False)

    conn_db_hostname = Column(String(1024), nullable=False)
    conn_db_port = Column(Integer, nullable=False)
    conn_db_username = Column(String(1024), nullable=False)
    conn_db_password = Column(String(1024), nullable=False)
    conn_db_name = Column(String(1024), nullable=False)
    
    start_transaction = Column(Boolean, default=True)
    delete_all_before_load = Column(Boolean, default=False)
    insert_record = Column(Boolean, default=True)
    update_record = Column(Boolean, default=False)
    use_column_maps_only = Column(Boolean, default=False)

    
    load_target_id = Column(Integer, ForeignKey('load_target.id'), nullable=False, unique=True)
    database_engine_id = Column(Integer, ForeignKey('database_engine.id'), nullable=False)

    load_target = relationship('LoadTarget', foreign_keys=[load_target_id])
    database_engine = relationship('DatabaseEngine', foreign_keys=[database_engine_id])


    def __repr__(self):
        return f"{self.conn_db_hostname} - {self.conn_db_port} - {self.conn_db_name} - {self.conn_db_username}"

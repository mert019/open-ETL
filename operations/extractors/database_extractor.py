import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from database.models.database_engine import DatabaseEngineEnum
from operations.extractors.extractor_base import BaseExtractor
from utils.database_utils import get_connection_url 


class DatabaseExtractor(BaseExtractor):


    def __init__(self, database_extract_config, operation_history, db) -> None:
        """
            Parameters:
                database_extract_config: DatabaseExtractConfig object.
                operation_history: OperationHistory object.
                db: SQLA database object.
        """
        super().__init__(db, operation_history)
        self.database_extract_config = database_extract_config
        self.query = database_extract_config.query
        self.database_connection = database_extract_config.database_connection

    
    def get_data(self):
        """Extracts data from data source."""
        data = None

        conn_url = get_connection_url(self.database_connection)
        engine = create_engine(conn_url)
        with engine.begin() as connection:
            data = pd.read_sql(self.query, connection)

        self.log_extract_amount(data.shape[0])
        data = self.rename_data_table_columns(True, data)

        return data

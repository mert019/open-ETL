import pandas as pd

from operations.extractors.extractor_base import BaseExtractor


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

        # connection info
        self.hostname = database_extract_config.conn_db_hostname
        self.port = database_extract_config.conn_db_port
        self.username = database_extract_config.conn_db_username
        self.password = database_extract_config.conn_db_password
        self.database = database_extract_config.conn_db_name


    def execute_query(self, conn):
        """
            Executes query and receives data table. 
            Returns extracted data as pandas.DataFrame.
            Parameters:
                conn: database connection object.
        """
        data = pd.read_sql(self.query, conn)
        self.log_extract_amount(data.shape[0])
        data = self.rename_data_table_columns(True, data)
        return data

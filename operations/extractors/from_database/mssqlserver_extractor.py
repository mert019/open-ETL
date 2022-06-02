import pymssql

from operations.extractors.from_database.database_extractor import DatabaseExtractor


class MSSQLServerExtractor(DatabaseExtractor):


    def __init__(self, database_extract_config, operation_history, db) -> None:
        super().__init__(database_extract_config, operation_history, db)


    def get_data(self):
        conn = pymssql.connect(
            server=self.hostname,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database)
        data = self.execute_query(conn)
        conn.close()
        return data

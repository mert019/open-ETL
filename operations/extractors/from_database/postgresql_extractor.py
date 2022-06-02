import psycopg2

from operations.extractors.from_database.database_extractor import DatabaseExtractor


class PostgresqlExtractor(DatabaseExtractor):

    def __init__(self, database_extract_config, operation_history, db) -> None:
        super().__init__(database_extract_config, operation_history, db)

    def get_data(self):
        conn = psycopg2.connect(
            host=self.hostname,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database)
        data = self.execute_query(conn)
        conn.close()
        return data

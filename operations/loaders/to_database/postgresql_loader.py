import psycopg2

from operations.loaders.to_database.database_loader import DatabaseLoader


class PostgresqlLoader(DatabaseLoader):


    def __init__(self, database_load_config, operation_history, db) -> None:
        super().__init__(database_load_config, operation_history, db)

        delete_query_template = 'DELETE FROM $TABLE_NAME$; '

        update_query_template = """
                IF EXISTS(SELECT 1 FROM $TABLE_NAME$ WHERE $WHERE_STATEMENT$) THEN
                    UPDATE $TABLE_NAME$
                    SET $SET_STATEMENT$
                    WHERE $WHERE_STATEMENT$;
                END IF;
            """

        insert_query_template = """INSERT INTO $TABLE_NAME$ ( $COLUMN_NAMES$ ) VALUES ( $INSERT_VALUES$ );"""

        upsert_query_template = """
                IF EXISTS(SELECT 1 FROM $TABLE_NAME$ WHERE $WHERE_STATEMENT$) THEN
                    UPDATE $TABLE_NAME$
                    SET $SET_STATEMENT$
                    WHERE $WHERE_STATEMENT$;
                ELSE
                    INSERT INTO $TABLE_NAME$ ( $COLUMN_NAMES$ ) VALUES( $INSERT_VALUES$ );
                END IF;
            """
                
        self.delete_query_template = delete_query_template
        self.update_query_template = update_query_template
        self.insert_query_template = insert_query_template
        self.upsert_query_template = upsert_query_template


    def load_data(self, df, load_columns):
        super(PostgresqlLoader, self).load_data(df, load_columns)

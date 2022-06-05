import psycopg2
import pymssql

from app.models.database_engine import DatabaseEngineEnum


def check_database_connection(database_config) -> str:
    """
        Checks database connection success using the given database configuration.
            Parameters:
                database_config:
                    DatabaseExtractConfig or DatabaseLoadConfig object.
            Returns:
                error_message: Returns error message if connection fails, otherwise returns None.
    """
    hostname = database_config.conn_db_hostname
    port = database_config.conn_db_port
    username = database_config.conn_db_username
    password = database_config.conn_db_password
    database = database_config.conn_db_name
    database_engine_id = database_config.database_engine.id
    
    try:
        conn = None

        if database_engine_id == DatabaseEngineEnum.MSSQLSERVER.value:
            conn = pymssql.connect(
                server=hostname,
                port=port,
                user=username,
                password=password,
                database=database)

        elif database_engine_id == DatabaseEngineEnum.POSTGRESQL.value:
            conn = psycopg2.connect(
                host=hostname,
                port=port,
                user=username,
                password=password,
                database=database)

        else:
            raise Exception(f"Database Engine could not matched for database engine id {database_engine_id}")

        conn.close()

    except Exception as ex:
        return str(ex)

    return None

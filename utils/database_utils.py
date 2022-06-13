from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from database.models.database_engine import DatabaseEngineEnum


def get_connection_url(database_config) -> URL:
    """
        Returns connection url for given database config.
        Parameters:
            database_config: DatabaseExtractConfig or DatabaseLoadConfig object.
    """
    database_engine_id = database_config.database_engine.id
    hostname = database_config.conn_db_hostname
    port = database_config.conn_db_port
    username = database_config.conn_db_username
    password = database_config.conn_db_password
    database = database_config.conn_db_name
    conn_url = None
    if database_engine_id == DatabaseEngineEnum.POSTGRESQL.value:
        conn_url = URL('postgresql+psycopg2', username, password, hostname, port, database)
    elif database_engine_id == DatabaseEngineEnum.MSSQLSERVER.value:
        conn_url = URL('mssql+pymssql', username, password, hostname, port, database)
    else:
        raise Exception("Database engine could not matched.")
    return conn_url


def check_database_connection(database_config) -> str:
    """
        Checks database connection success using the given database configuration.
            Parameters:
                database_config:
                    DatabaseExtractConfig or DatabaseLoadConfig object.
            Returns:
                error_message: Returns error message if connection fails, otherwise returns None.
    """
    try:
        conn_url = get_connection_url(database_config)
        engine = create_engine(conn_url)
        connection = engine.connect()
        connection.close()
    except Exception as ex:
        return str(ex)
    return None

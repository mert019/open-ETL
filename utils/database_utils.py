from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

from database.models.database_engine import DatabaseEngineEnum
from database.models.database_connection import DatabaseConnection


def get_connection_url(database_conn:DatabaseConnection) -> URL:
    """
        Returns connection url for given database connection.
        Parameters:
            database_conn: DatabaseConnection object.
    """
    database_engine_id = database_conn.database_engine.id
    hostname = database_conn.conn_db_hostname
    port = database_conn.conn_db_port
    username = database_conn.conn_db_username
    password = database_conn.conn_db_password
    database = database_conn.conn_db_name
    conn_url = None
    if database_engine_id == DatabaseEngineEnum.POSTGRESQL.value:
        conn_url = URL('postgresql+psycopg2', username, password, hostname, port, database)
    elif database_engine_id == DatabaseEngineEnum.MSSQLSERVER.value:
        conn_url = URL('mssql+pymssql', username, password, hostname, port, database)
    else:
        raise Exception("Database engine could not matched.")
    return conn_url


def check_database_connection(database_conn:DatabaseConnection) -> str:
    """
        Checks database connection success using the given database connection.
            Parameters:
                database_conn:
                    DatabaseConnection object.
            Returns:
                error_message: Returns error message if connection fails, otherwise returns None.
    """
    conn_url = get_connection_url(database_conn)
    return check_database_connection_from_url(conn_url)


def check_database_connection_from_url(conn_url):
    """
        Checks database connection success using the given connection url.
            Parameters:
                conn_url: Database connection url.
            Returns:
                error_message: Returns error message if connection fails, otherwise returns None.
    """
    try:
        engine = create_engine(conn_url)
        connection = engine.connect()
        connection.close()
    except Exception as ex:
        return str(ex)
    return None

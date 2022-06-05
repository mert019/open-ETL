from ftplib import FTP
import paramiko
import psycopg2
import pymssql

from app.models.database_engine import DatabaseEngineEnum
from app.models.ftp_type import FTPTypeEnum


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


def check_ftp_connection(ftp_config):
    """
        Checks ftp/sftp connection success using the given ftp configuration.
            Parameters:
                ftp_config:
                    ExcelExtractConfig or CSVExtractConfig object.
            Returns:
                error_message: Returns error message if connection fails, otherwise returns None.
    """
    hostname = ftp_config.ftp_hostname
    port = ftp_config.ftp_port
    username = ftp_config.ftp_username
    password = ftp_config.ftp_password
    ftp_type_id = ftp_config.ftp_type_id

    try:

        if ftp_type_id == FTPTypeEnum.FTP.value:
            ftp_server = FTP()
            ftp_server.connect(hostname, port)
            ftp_server.login(username, password)
            ftp_server.close()
            
        elif ftp_type_id == FTPTypeEnum.SFTP.value:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, port, username, password)
            ssh.close()
            
        else:
            raise Exception(f"FTP type could not matched for ftp type id {ftp_type_id}")

    except Exception as ex:
        return str(ex)

    return None

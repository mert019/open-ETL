from database import db

from database.models.database_engine import DatabaseEngine, DatabaseEngineEnum
from database.models.ftp_type import FTPType
from database.models.column_data_type import ColumnDataType
from database.models.extract_source import ExtractSource
from database.models.database_extract_config import DatabaseExtractConfig
from database.models.database_load_config import DatabaseLoadConfig
from database.models.extract_column import ExtractColumn
from database.models.extract_type import ExtractType, ExtractTypeEnum
from database.models.load_target import LoadTarget
from database.models.load_type import LoadType
from database.models.operation_config import OperationConfig
from database.models.operation_history import OperationHistory
from database.models.operation_history_log import OperationHistoryLog
from database.models.operation_log_type import OperationLogType
from database.models.excel_extract_config import ExcelExtractConfig
from database.models.csv_extract_config import CSVExtractConfig
from database.models.schedule_unit import ScheduleUnit
from database.models.extract_file import ExtractFile


# EXTRACT SOURCE

# Postgres
postgres_extract_source = ExtractSource()
postgres_extract_source.extract_source_name = "Postgres test extract source"
postgres_extract_source.extract_type_id = ExtractTypeEnum.FROM_DATABASE.value
db.session.add(postgres_extract_source)
db.session.commit()

# MSSQLServer
mssqlserver_extract_source = ExtractSource()
mssqlserver_extract_source.extract_source_name = "MSSQLServer test extract source"
mssqlserver_extract_source.extract_type_id = ExtractTypeEnum.FROM_DATABASE.value
db.session.add(mssqlserver_extract_source)
db.session.commit()

# SFTP Excel
excel_extract_source = ExtractSource()
excel_extract_source.extract_source_name = "MSSQLServer test extract source"
excel_extract_source.extract_type_id = ExtractTypeEnum.FROM_EXCEL.value
db.session.add(excel_extract_source)
db.session.commit()



# DATABASE EXTRACT CONFIG

# MSSQLServer
mssql_database_extract_config = DatabaseExtractConfig()
mssql_database_extract_config.extract_source_id = mssqlserver_extract_source.id
mssql_database_extract_config.conn_db_hostname = "localhost"
mssql_database_extract_config.conn_db_name = "MockSQLServerLoadDB"
mssql_database_extract_config.conn_db_password = "Password@123456"
mssql_database_extract_config.conn_db_port = 9001
mssql_database_extract_config.conn_db_username = "sa"
mssql_database_extract_config.database_engine_id = DatabaseEngineEnum.MSSQLSERVER.value
mssql_database_extract_config.query = "SELECT [id] ,[first_name] ,[email] ,[ip_address] ,[is_enabled] ,[join_date] ,[point] FROM [myTable];"
db.session.add(mssql_database_extract_config)
db.session.commit()

# Postgres
pg_database_extract_config = DatabaseExtractConfig()
pg_database_extract_config.extract_source_id = postgres_extract_source.id
pg_database_extract_config.conn_db_hostname = "localhost"
pg_database_extract_config.conn_db_name = "MockPGDatabase"
pg_database_extract_config.conn_db_password = "postgres123456"
pg_database_extract_config.conn_db_port = 9000
pg_database_extract_config.conn_db_username = "postgres"
pg_database_extract_config.database_engine_id = DatabaseEngineEnum.POSTGRESQL.value
pg_database_extract_config.query = "SELECT * FROM public.mytable;"
db.session.add(pg_database_extract_config)
db.session.commit()

# EXCEL EXTRACT CONFIG
xlsx_extarct_config = ExcelExtractConfig()
xlsx_extarct_config.extract_directory = '/home/foo/upload'
xlsx_extarct_config.extract_source_id = excel_extract_source.id
xlsx_extarct_config.ftp_hostname = "localhost"
xlsx_extarct_config.ftp_password = "pass"
xlsx_extarct_config.
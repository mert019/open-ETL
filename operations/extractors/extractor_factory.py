from app.models.database_extract_config import DatabaseExtractConfig
from app.models.excel_extract_config import ExcelExtractConfig
from app.models.csv_extract_config import CSVExtractConfig
from app.models.database_engine import DatabaseEngineEnum
from app.models.extract_type import ExtractTypeEnum

from operations.extractors.from_database.postgresql_extractor import PostgresqlExtractor
from operations.extractors.from_database.mssqlserver_extractor import MSSQLServerExtractor
from operations.extractors.from_ftp.excel_extractor import ExcelExtractor
from operations.extractors.from_ftp.csv_extractor import CSVExtractor


def extractor_factory(extract_source, operation_history, db):
    """
        Parameters:
            extract_source: ExtractSource
            db: SQLA
        Returns an BaseExtractor type class.
    """
    extractor = None
    
    # FROM_DATABASE
    if extract_source.extract_type_id == ExtractTypeEnum.FROM_DATABASE.value:
        database_extract_config = db.session.query(DatabaseExtractConfig).filter_by(extract_source_id=extract_source.id).first()
        database_engine = database_extract_config.database_engine

        if database_engine.id == DatabaseEngineEnum.POSTGRESQL.value:
            extractor = PostgresqlExtractor(database_extract_config, operation_history, db)
        elif database_engine.id == DatabaseEngineEnum.MSSQLSERVER.value:
            extractor = MSSQLServerExtractor(database_extract_config, operation_history, db)
        else:
            raise ValueError(f"Database engine for DatabaseExtractConfig {database_extract_config.id} could not matched.")

    # FROM_EXCEL
    elif extract_source.extract_type_id == ExtractTypeEnum.FROM_EXCEL.value:
        excel_extract_config = db.session.query(ExcelExtractConfig).filter_by(extract_source_id=extract_source.id).first()
        extractor = ExcelExtractor(excel_extract_config, operation_history, db)

    # FROM_CSV
    elif extract_source.extract_type_id == ExtractTypeEnum.FROM_CSV.value:
        csv_extract_config = db.session.query(CSVExtractConfig).filter_by(extract_source_id=extract_source.id).first()
        extractor = CSVExtractor(csv_extract_config, operation_history, db)

    else:
        raise ValueError(f"Extract type for extract source {repr(extract_source)} could not identified.")

    return extractor

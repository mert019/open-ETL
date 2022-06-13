from database.models.database_extract_config import DatabaseExtractConfig
from database.models.excel_extract_config import ExcelExtractConfig
from database.models.csv_extract_config import CSVExtractConfig
from database.models.database_engine import DatabaseEngineEnum
from database.models.extract_type import ExtractTypeEnum
from database.models.operation_history import OperationHistory

from operations.extractors.database_extractor import DatabaseExtractor
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
        extractor = DatabaseExtractor(database_extract_config, operation_history, db)

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

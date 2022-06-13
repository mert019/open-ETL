from flask import jsonify
from flask_appbuilder import has_access
from flask_appbuilder.api import BaseApi, expose

from app import appbuilder, db

from database.models.column_data_type import ColumnDataType
from database.models.csv_extract_config import CSVExtractConfig
from database.models.database_engine import DatabaseEngine
from database.models.database_extract_config import DatabaseExtractConfig
from database.models.database_load_config import DatabaseLoadConfig
from database.models.excel_extract_config import ExcelExtractConfig
from database.models.extract_column import ExtractColumn
from database.models.extract_source import ExtractSource
from database.models.extract_type import ExtractType, ExtractTypeEnum
from database.models.load_target import LoadTarget
from database.models.load_type import LoadType, LoadTypeEnum
from database.models.operation_config import OperationConfig
from database.models.operation_history import OperationHistory
from database.models.operation_history_log import OperationHistoryLog
from database.models.operation_log_type import OperationLogType


class DropdownFeederApi(BaseApi):

    @expose('/databaseextractconfig_extractsourcefeed')
    @has_access
    def database_extract_config_extract_source_feed(self):
        """
            database_extract_config_extract_source_feed finds all the unassigned ExtractSources whose extract type is FROM_DATABASE.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        db_extract_configs = db.session.query(DatabaseExtractConfig).all()

        db_extract_config_source_ids = []
        for obj in db_extract_configs:
            db_extract_config_source_ids.append(obj.extract_source_id)

        extract_sources = db.session.query(ExtractSource).filter(
            ExtractSource.id.notin_(db_extract_config_source_ids) 
            & (ExtractSource.extract_type_id == ExtractTypeEnum.FROM_DATABASE.value)).all()

        response_val = []
        for obj in extract_sources:
            response_val.append({"id": obj.id, "text": repr(obj)})

        return jsonify(response_val)


    @expose('/databaseloadconfig_loadtargetfeed')
    @has_access
    def database_load_config_load_target_feed(self):
        """
            database_load_config_load_source_feed finds all the unassigned LoadTargets whose extract type is FROM_DATABASE.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        db_load_configs = db.session.query(DatabaseLoadConfig).all()

        db_load_config_source_ids = []
        for obj in db_load_configs:
            db_load_config_source_ids.append(obj.load_target_id)

        load_targets = db.session.query(LoadTarget).filter(
            LoadTarget.id.notin_(db_load_config_source_ids) 
            & (LoadTarget.load_type_id == LoadTypeEnum.TO_DATABASE.value)).all()

        response_val = []
        for obj in load_targets:
            response_val.append({"id": obj.id, "text": repr(obj)})

        return jsonify(response_val)

    
    @expose('/excelextractconfig_extractsourcefeed')
    @has_access
    def excel_extract_config_extract_source_feed(self):
        """
            excel_extract_config_extract_source_feed finds all the unassigned ExtractSources whose extract type is FROM_EXCEL.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        excel_extract_configs = db.session.query(ExcelExtractConfig).all()

        excel_extract_config_source_ids = []
        for obj in excel_extract_configs:
            excel_extract_config_source_ids.append(obj.extract_source_id)

        extract_sources = db.session.query(ExtractSource).filter(
            ExtractSource.id.notin_(excel_extract_config_source_ids) 
            & (ExtractSource.extract_type_id == ExtractTypeEnum.FROM_EXCEL.value)).all()

        response_val = []
        for obj in extract_sources:
            response_val.append({"id": obj.id, "text": repr(obj)})

        return jsonify(response_val)

    
    @expose('/csvextractconfig_extractsourcefeed')
    @has_access
    def csv_extract_config_extract_source_feed(self):
        """
            csv_extract_config_extract_source_feed finds all the unassigned ExtractSources whose extract type is FROM_CSV.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        csv_extract_configs = db.session.query(CSVExtractConfig).all()

        csv_extract_config_source_ids = []
        for obj in csv_extract_configs:
            csv_extract_config_source_ids.append(obj.extract_source_id)

        extract_sources = db.session.query(ExtractSource).filter(
            ExtractSource.id.notin_(csv_extract_config_source_ids) 
            & (ExtractSource.extract_type_id == ExtractTypeEnum.FROM_CSV.value)).all()

        response_val = []
        for obj in extract_sources:
            response_val.append({"id": obj.id, "text": repr(obj)})

        return jsonify(response_val)


appbuilder.add_api(DropdownFeederApi)

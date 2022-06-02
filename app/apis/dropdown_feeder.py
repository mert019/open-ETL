from flask import jsonify
from flask_appbuilder import has_access
from flask_appbuilder.api import BaseApi, expose

from app import appbuilder, db

from app.models.column_data_type import ColumnDataType
from app.models.column_map import ColumnMap
from app.models.csv_extract_config import CSVExtractConfig
from app.models.database_engine import DatabaseEngine
from app.models.database_extract_config import DatabaseExtractConfig
from app.models.database_load_config import DatabaseLoadConfig
from app.models.excel_extract_config import ExcelExtractConfig
from app.models.extract_column import ExtractColumn
from app.models.extract_source import ExtractSource
from app.models.extract_type import ExtractType, ExtractTypeEnum
from app.models.load_column import LoadColumn
from app.models.load_target import LoadTarget
from app.models.load_type import LoadType, LoadTypeEnum
from app.models.operation_config import OperationConfig
from app.models.operation_history import OperationHistory
from app.models.operation_history_log import OperationHistoryLog
from app.models.operation_log_type import OperationLogType


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


    @expose('/operation_config_extract_source')
    @has_access
    def operation_config_extract_source_feed(self):
        """
            operation_config_extract_source_feed finds all the unassigned ExtractSource for OperationConfig.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        assigned_extract_sources = db.session.query(OperationConfig).all()
        assigned_extract_source_ids = []

        for obj in assigned_extract_sources:
            assigned_extract_source_ids.append(obj.extract_source.id)

        extract_sources = db.session.query(ExtractSource).filter(
            ExtractSource.id.notin_(assigned_extract_source_ids)).all()

        response_val = []
        for obj in extract_sources:
            response_val.append({"id": obj.id, "text": repr(obj)})

        return jsonify(response_val)

    
    @expose('/operation_config_load_target')
    @has_access
    def operation_config_load_target_feed(self):
        """
            operation_config_load_target_feed finds all the unassigned LoadTarget for OperationConfig.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        assigned_load_targets = db.session.query(OperationConfig).all()
        assigned_load_target_ids = []

        for obj in assigned_load_targets:
            assigned_load_target_ids.append(obj.extract_source.id)

        extract_sources = db.session.query(LoadTarget).filter(
            LoadTarget.id.notin_(assigned_load_target_ids)).all()

        response_val = []
        for obj in extract_sources:
            response_val.append({"id": obj.id, "text": repr(obj)})

        return jsonify(response_val)


    @expose('columnmap_extractcolumn/<oper_id>')
    @has_access
    def column_map_extract_column_feed(self, oper_id):
        """
            column_map_extract_column_feed finds all the unassigned extract columns for the given operation config id.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        oper_id = int(oper_id)

        operation_config = db.session.query(OperationConfig).filter_by(id=oper_id).first()

        extract_source_id = operation_config.extract_source_id

        column_maps = db.session.query(ColumnMap).filter(
            ColumnMap.operation_config_id == oper_id).all()

        mapped_extract_source_column_ids = []
        for obj in column_maps:
            mapped_extract_source_column_ids.append(obj.extract_column_id)

        extract_columns = db.session.query(ExtractColumn).filter(
            (ExtractColumn.extract_source_id == extract_source_id)
            & ExtractColumn.id.notin_(mapped_extract_source_column_ids)).all()

        response_val = []
        for obj in extract_columns:
            response_val.append({"id": obj.id, "text": repr(obj)})

        return jsonify(response_val)


    @expose('columnmap_loadcolumn/<oper_id>')
    @has_access
    def column_map_load_column_feed(self, oper_id):
        """
            column_map_load_column_feed finds all the unassigned load columns for the given operation config id.
            Returns a list of dictionary. Dictionary keys are id & text.
        """
        oper_id = int(oper_id)

        operation_config = db.session.query(OperationConfig).filter_by(id=oper_id).first()

        load_target_id = operation_config.load_target_id

        column_maps = db.session.query(ColumnMap).filter(
            ColumnMap.operation_config_id == oper_id).all()

        mapped_load_target_column_ids = []
        for obj in column_maps:
            mapped_load_target_column_ids.append(obj.load_column_id)

        load_columns = db.session.query(LoadColumn).filter(
            (LoadColumn.load_target_id == load_target_id)
            & LoadColumn.id.notin_(mapped_load_target_column_ids)).all()

        response_val = []
        for obj in load_columns:
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

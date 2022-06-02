from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, BS3PasswordFieldWidget, Select2AJAXWidget

from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired

from app import appbuilder

from app.models.column_data_type import ColumnDataType
from app.models.csv_extract_config import CSVExtractConfig
from app.models.database_engine import DatabaseEngine
from app.models.database_extract_config import DatabaseExtractConfig
from app.models.excel_extract_config import ExcelExtractConfig
from app.models.extract_column import ExtractColumn
from app.models.extract_source import ExtractSource
from app.models.extract_type import ExtractType
from app.models.ftp_type import FTPType


EXTRACT_CATEGORY_NAME = "Extract"


class ExtractSourceModelView(ModelView):
    datamodel = SQLAInterface(ExtractSource)
    related_views = [ExtractSource, ExtractType]

    list_columns = ['extract_source_name', 'extract_type']

    add_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget())
    }

    edit_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget())
    }

appbuilder.add_view(ExtractSourceModelView, "Manage Extract Sources", category=EXTRACT_CATEGORY_NAME)


class DatabaseExtractConfigModelView(ModelView):
    datamodel = SQLAInterface(DatabaseExtractConfig)
    related_views = [DatabaseExtractConfig, DatabaseEngine]

    edit_columns = ['database_engine', 'conn_db_hostname', 'conn_db_port', 'conn_db_username', 'conn_db_password', 'conn_db_name', 'query']

    add_form_extra_fields = {
        'conn_db_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget()),

        'extract_source': AJAXSelectField('Extract Source',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='extract_source',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/databaseextractconfig_extractsourcefeed')),
    }


appbuilder.add_view(DatabaseExtractConfigModelView, "Database Configurations", category=EXTRACT_CATEGORY_NAME)


class ExcelExtractConfigModelView(ModelView):
    datamodel = SQLAInterface(ExcelExtractConfig)
    related_views = [ExcelExtractConfig, FTPType]

    edit_columns = ['ftp_type', 'ftp_hostname', 'ftp_port', 'ftp_username', 'ftp_password', 'extract_directory',
     'read_file_name', 'read_file_name_regex', 'table_start_index', 'ignore_last_n_rows', 'has_headers']

    add_form_extra_fields = {
        'ftp_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget()),

        'extract_source': AJAXSelectField('Extract Source',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='extract_source',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/excelextractconfig_extractsourcefeed')),
    }


appbuilder.add_view(ExcelExtractConfigModelView, "Excel Configurations", category=EXTRACT_CATEGORY_NAME)


class CSVExtractConfigModelView(ModelView):
    datamodel = SQLAInterface(CSVExtractConfig)
    related_views = [CSVExtractConfig, FTPType]

    edit_columns = ['ftp_type', 'ftp_hostname', 'ftp_port', 'ftp_username', 'ftp_password', 'extract_directory',
     'read_file_name', 'read_file_name_regex', 'seperator', 'table_start_index', 'ignore_last_n_rows', 'has_headers']

    add_form_extra_fields = {
        'ftp_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget()),

        'extract_source': AJAXSelectField('Extract Source',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='extract_source',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/csvextractconfig_extractsourcefeed')),
    }


appbuilder.add_view(CSVExtractConfigModelView, "CSV Configurations", category=EXTRACT_CATEGORY_NAME)


class ExtractColumnModelView(ModelView):
    datamodel = SQLAInterface(ExtractColumn)
    related_views = [ExtractColumn, ColumnDataType, ExtractSource]
    list_columns = ['extract_source', 'column_name', 'column_data_type']

appbuilder.add_view(ExtractColumnModelView, "Manage Columns", category=EXTRACT_CATEGORY_NAME)

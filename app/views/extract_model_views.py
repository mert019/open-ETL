from flask import flash, redirect

from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, BS3PasswordFieldWidget, Select2AJAXWidget

from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired

from app import appbuilder

from database.models.column_data_type import ColumnDataType
from database.models.database_connection import DatabaseConnection
from database.models.ftp_connection import FtpConnection
from database.models.csv_extract_config import CSVExtractConfig
from database.models.database_engine import DatabaseEngine
from database.models.database_extract_config import DatabaseExtractConfig
from database.models.excel_extract_config import ExcelExtractConfig
from database.models.extract_column import ExtractColumn
from database.models.extract_source import ExtractSource
from database.models.extract_type import ExtractType
from database.models.ftp_type import FTPType

from utils.database_utils import check_database_connection
from utils.ftp_utils import check_ftp_connection


EXTRACT_CATEGORY_NAME = "Extract"


class ExtractSourceModelView(ModelView):
    datamodel = SQLAInterface(ExtractSource)
    related_views = [ExtractSource, ExtractType]

    list_columns = ['extract_source_name', 'extract_type']

    edit_columns = ['extract_source_name']

appbuilder.add_view(ExtractSourceModelView, "Manage Extract Sources", category=EXTRACT_CATEGORY_NAME)


class DatabaseExtractConfigModelView(ModelView):
    datamodel = SQLAInterface(DatabaseExtractConfig)
    related_views = [DatabaseExtractConfig, DatabaseConnection]

    edit_columns = ['database_connection', 'query']

    add_form_extra_fields = {
        'extract_source': AJAXSelectField('Extract Source',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='extract_source',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/databaseextractconfig_extractsourcefeed')),

        'query': TextAreaField(widget=BS3TextAreaFieldWidget()),
    }

    edit_form_extra_fields = {
        'query': TextAreaField(widget=BS3TextAreaFieldWidget()),
    }

    @action("test_connection", "Test Connection", confirmation=None, icon="fa-signal", multiple=False)
    def test_connection(self, item):
        error_message = check_database_connection(item.database_connection)
        if error_message:
            flash(f"ERROR: {error_message}", 'warning')
        else:
            flash("Connection successful.", 'success')
        return redirect(f"/databaseextractconfigmodelview/show/{item.id}")

appbuilder.add_view(DatabaseExtractConfigModelView, "Database Configurations", category=EXTRACT_CATEGORY_NAME)


class ExcelExtractConfigModelView(ModelView):
    datamodel = SQLAInterface(ExcelExtractConfig)
    related_views = [ExcelExtractConfig, FtpConnection]

    edit_columns = ['ftp_connection', 'extract_directory', 'read_file_name', 'read_file_name_regex', 'table_start_index', 'ignore_last_n_rows', 'has_headers']

    label_columns = {
        "extract_directory": "Remote Directory",
        "read_file_name": "Remote File Name",
        "read_file_name_regex": "Filter File Names with Regex",
        "has_headers": "Has Header Row",
        "extract_source": "Extract Source",
    }

    add_form_extra_fields = {
        'extract_source': AJAXSelectField('Extract Source',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='extract_source',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/excelextractconfig_extractsourcefeed')),
    }

    @action("test_connection", "Test Connection", confirmation=None, icon="fa-signal", multiple=False)
    def test_connection(self, item):
        error_message = check_ftp_connection(item.ftp_connection)
        if error_message:
            flash(f"ERROR: {error_message}", 'warning')
        else:
            flash("Connection successful.", 'success')
        return redirect(f"/excelextractconfigmodelview/show/{item.id}")

appbuilder.add_view(ExcelExtractConfigModelView, "Excel Configurations", category=EXTRACT_CATEGORY_NAME)


class CSVExtractConfigModelView(ModelView):
    datamodel = SQLAInterface(CSVExtractConfig)
    related_views = [CSVExtractConfig, FtpConnection]

    edit_columns = ['ftp_connection', 'extract_directory', 'read_file_name', 'read_file_name_regex', 'seperator', 'table_start_index', 'ignore_last_n_rows', 'has_headers']

    label_columns = {
        "extract_directory": "Remote Directory",
        "read_file_name": "Remote File Name",
        "read_file_name_regex": "Filter File Names with Regex",
        "has_headers": "Has Header Row",
        "extract_source": "Extract Source",
    }

    add_form_extra_fields = {
        'extract_source': AJAXSelectField('Extract Source',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='extract_source',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/csvextractconfig_extractsourcefeed')),
    }
    
    @action("test_connection", "Test Connection", confirmation=None, icon="fa-signal", multiple=False)
    def test_connection(self, item):
        error_message = check_ftp_connection(item.ftp_connection)
        if error_message:
            flash(f"ERROR: {error_message}", 'warning')
        else:
            flash("Connection successful.", 'success')
        return redirect(f"/csvextractconfigmodelview/show/{item.id}")

appbuilder.add_view(CSVExtractConfigModelView, "CSV Configurations", category=EXTRACT_CATEGORY_NAME)


class ExtractColumnModelView(ModelView):
    datamodel = SQLAInterface(ExtractColumn)
    related_views = [ExtractColumn, ColumnDataType, ExtractSource]
    list_columns = ['extract_source', 'column_name', 'column_data_type', 'column_index']

appbuilder.add_view(ExtractColumnModelView, "Manage Columns", category=EXTRACT_CATEGORY_NAME)

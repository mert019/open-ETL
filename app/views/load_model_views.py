from flask import flash, redirect

from flask_appbuilder.actions import action
from flask_appbuilder import ModelView
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, BS3PasswordFieldWidget, Select2AJAXWidget
from flask_appbuilder.models.sqla.interface import SQLAInterface

from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired

from app import appbuilder

from database.models.column_data_type import ColumnDataType
from database.models.database_connection import DatabaseConnection
from database.models.database_load_config import DatabaseLoadConfig
from database.models.load_column import LoadColumn
from database.models.load_target import LoadTarget
from database.models.load_type import LoadType

from utils.database_utils import check_database_connection


LOAD_CATEGORY_NAME = "Load"


class LoadTargetModelView(ModelView):
    datamodel = SQLAInterface(LoadTarget)
    related_views = [LoadTarget, LoadType]

    list_columns = ['load_target_name', 'load_type']

    edit_columns = ['load_target_name']

appbuilder.add_view(LoadTargetModelView, "Manage Load Targets", category=LOAD_CATEGORY_NAME)


class DatabaseLoadConfigModelView(ModelView):
    datamodel = SQLAInterface(DatabaseLoadConfig)
    related_views = [DatabaseLoadConfig, DatabaseConnection]

    edit_columns = ['database_connection', 'table_name', 'delete_all_before_load', 'insert_record', 'update_record', 'start_transaction']

    add_form_extra_fields = {
        'load_target': AJAXSelectField('Load Target',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='load_target',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/databaseloadconfig_loadtargetfeed')),
    }

    @action("test_connection", "Test Connection", confirmation=None, icon="fa-signal", multiple=False)
    def test_connection(self, item):
        error_message = check_database_connection(item.database_connection)
        if error_message:
            flash(f"ERROR: {error_message}", 'warning')
        else:
            flash("Connection successful.", 'success')
        return redirect(f"/databaseloadconfigmodelview/show/{item.id}")

appbuilder.add_view(DatabaseLoadConfigModelView, "Database Configuration", category=LOAD_CATEGORY_NAME)


class LoadColumnModelView(ModelView):
    datamodel = SQLAInterface(LoadColumn)
    related_views = [LoadColumn, ColumnDataType, LoadTarget]

    list_columns = ['load_target', 'column_name', 'column_data_type', 'is_makes_record_unique']

appbuilder.add_view(LoadColumnModelView, "Manage Columns", category=LOAD_CATEGORY_NAME)

from flask_appbuilder import ModelView
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, BS3PasswordFieldWidget, Select2AJAXWidget
from flask_appbuilder.models.sqla.interface import SQLAInterface

from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired


from app import appbuilder

from app.models.column_data_type import ColumnDataType
from app.models.database_engine import DatabaseEngine
from app.models.database_load_config import DatabaseLoadConfig
from app.models.load_column import LoadColumn
from app.models.load_target import LoadTarget
from app.models.load_type import LoadType


LOAD_CATEGORY_NAME = "Load"


class LoadTargetModelView(ModelView):
    datamodel = SQLAInterface(LoadTarget)
    related_views = [LoadTarget, LoadType]

    list_columns = ['load_target_name', 'load_type']

    add_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget())
    }

    edit_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget())
    }

appbuilder.add_view(LoadTargetModelView, "Manage Load Targets", category=LOAD_CATEGORY_NAME)


class DatabaseLoadConfigModelView(ModelView):
    datamodel = SQLAInterface(DatabaseLoadConfig)
    related_views = [DatabaseLoadConfig, DatabaseEngine]

    edit_columns = ['database_engine', 'table_name', 'conn_db_hostname', 'conn_db_port', 'conn_db_username', 'conn_db_password', 'conn_db_name', 'start_transaction',
                        'delete_all_before_load', 'insert_record', 'update_record', 'use_column_maps_only',]

    add_form_extra_fields = {
        'conn_db_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget()),

        'load_target': AJAXSelectField('Load Target',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='load_target',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/databaseloadconfig_loadtargetfeed')),
    }


appbuilder.add_view(DatabaseLoadConfigModelView, "Database Configuration", category=LOAD_CATEGORY_NAME)


class LoadColumnModelView(ModelView):
    datamodel = SQLAInterface(LoadColumn)
    related_views = [LoadColumn, ColumnDataType, LoadTarget]

    list_columns = ['load_target', 'column_name', 'column_data_type', 'is_makes_record_unique']

appbuilder.add_view(LoadColumnModelView, "Manage Columns", category=LOAD_CATEGORY_NAME)

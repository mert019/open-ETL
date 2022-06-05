from flask import flash, redirect

from flask_appbuilder.actions import action
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, Select2AJAXWidget, Select2SlaveAJAXWidget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView

from wtforms import TextAreaField
from wtforms.validators import DataRequired

from app import appbuilder

from app.models.extract_column import ExtractColumn
from app.models.extract_source import ExtractSource
from app.models.operation_config import OperationConfig
from app.models.column_map import ColumnMap
from app.models.load_target import LoadTarget

from operations import operation_scheduler


OPERATION_CATEGORY_NAME = "Operation"


class OperationConfigModelView(ModelView):
    datamodel = SQLAInterface(OperationConfig)
    related_views = [OperationConfig, ExtractSource, LoadTarget]

    add_columns = ['operation_name', 'extract_source', 'load_target', 'description', 'schedule_unit', 'schedule_interval']

    edit_columns = ['operation_name', 'description', 'is_enabled', 'schedule_unit', 'schedule_interval']
    
    list_columns = ['operation_name', 'extract_source', 'load_target', 'is_enabled', 'schedule_unit', 'schedule_interval']

    show_columns = ['operation_name', 'extract_source', 'load_target', 'is_enabled', 'schedule_unit', 'schedule_interval']

    add_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget()),

        'extract_source': AJAXSelectField('Extract Source',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='extract_source',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/operation_config_extract_source')),

        'load_target': AJAXSelectField('Load Target',
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='load_target',
            widget=Select2AJAXWidget(endpoint='/api/v1/dropdownfeederapi/operation_config_load_target')),
    }

    edit_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget())
    }

    @action("run_operation", "Run Now", confirmation="Are you sure you want to run this operation?", icon="fa-play", multiple=False)
    def run_operation(self, item):
        if item.is_in_process:
            flash("Operation currently is in process.", 'warning')
            return redirect(f"/operationconfigmodelview/show/{item.id}")
        else:
            operation_history_id = operation_scheduler.add_operation_to_queue(item)
            flash("Operation added to queue.", 'success')
            return redirect(f"/operationhistorylogmodelview/list/?_flt_0_operation_history={operation_history_id}")

appbuilder.add_view(OperationConfigModelView, "Manage Operations", category=OPERATION_CATEGORY_NAME)


class ColumnMapModelView(ModelView):
    datamodel = SQLAInterface(ColumnMap)
    related_views = [ColumnMap, ExtractColumn]

    add_columns = ['operation_config', 'extract_column', 'load_column']

    list_columns = ['operation_config', 'extract_column', 'load_column']

    show_columns = ['operation_config', 'extract_column', 'load_column']

    add_form_extra_fields = {

        'operation_config': AJAXSelectField('Operation',
            id="operation_config_dropdownlist_id",
            validators=[DataRequired()],
            datamodel=datamodel,
            col_name='operation_config',
            widget=Select2AJAXWidget(endpoint='/columnmapmodelview/api/column/add/operation_config')),

        'extract_column': AJAXSelectField('Extract Column',
            datamodel=datamodel,
            validators=[DataRequired()],
            description="You need to choose operation first. Shows unmapped extract columns.",
            col_name='extract_column',
            widget=Select2SlaveAJAXWidget(master_id='operation_config_dropdownlist_id',
            endpoint='/api/v1/dropdownfeederapi/columnmap_extractcolumn/{{ID}}')),

        'load_column': AJAXSelectField('Load Column',
            datamodel=datamodel,
            description="You need to choose operation first. Shows unmapped load columns.",
            validators=[DataRequired()],
            col_name='load_column',
            widget=Select2SlaveAJAXWidget(master_id='operation_config_dropdownlist_id',
            endpoint='/api/v1/dropdownfeederapi/columnmap_loadcolumn/{{ID}}')),
    }


appbuilder.add_view(ColumnMapModelView, "Map Columns", category=OPERATION_CATEGORY_NAME)

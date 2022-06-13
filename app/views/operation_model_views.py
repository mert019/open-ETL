from flask import flash, redirect

from flask_appbuilder.actions import action
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, Select2AJAXWidget, Select2SlaveAJAXWidget
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView

from wtforms import TextAreaField
from wtforms.validators import DataRequired

from app import appbuilder

from database.models.extract_column import ExtractColumn
from database.models.extract_source import ExtractSource
from database.models.operation_config import OperationConfig
from database.models.load_target import LoadTarget

from operations import operation_scheduler


OPERATION_CATEGORY_NAME = "Operation"


class OperationConfigModelView(ModelView):
    datamodel = SQLAInterface(OperationConfig)
    related_views = [OperationConfig, ExtractSource, LoadTarget]

    add_columns = ['operation_name', 'extract_source', 'load_target', 'description', 'is_schedule_enabled', 'schedule_unit', 'schedule_interval', 'transform_query']

    edit_columns = ['operation_name', 'extract_source', 'load_target',  'description', 'is_schedule_enabled', 'schedule_unit', 'schedule_interval', 'transform_query']
    
    list_columns = ['operation_name', 'extract_source', 'load_target', 'is_schedule_enabled', 'schedule_unit', 'schedule_interval']

    show_columns = ['operation_name', 'extract_source', 'load_target', 'is_schedule_enabled', 'schedule_unit', 'schedule_interval', 'transform_query']

    add_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget()),

        'transform_query': TextAreaField(
            widget=BS3TextAreaFieldWidget()),
    }

    edit_form_extra_fields = {
        'description': TextAreaField(
            widget=BS3TextAreaFieldWidget()),

        'transform_query': TextAreaField(
            widget=BS3TextAreaFieldWidget()),
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

    @action("view_operation_history", "History", confirmation=None, icon=None, multiple=False)
    def view_operation_history(self, item):
        return redirect(f"/operationhistorymodelview/list/?_flt_0_operation_config={item.id}&_oc_OperationHistoryModelView=id&_od_OperationHistoryModelView=desc")

appbuilder.add_view(OperationConfigModelView, "Manage Operations", category=OPERATION_CATEGORY_NAME)

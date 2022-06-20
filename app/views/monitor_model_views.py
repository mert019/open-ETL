from flask import flash, redirect, render_template

from flask_appbuilder.actions import action
from flask_appbuilder import ModelView, BaseView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder

from config import SQLALCHEMY_DATABASE_URI, STAGING_DATABASE_URI

from database import db

from database.models.extract_file import ExtractFile
from database.models.operation_history import OperationHistory
from database.models.operation_config import OperationConfig
from database.models.operation_history_log import OperationHistoryLog
from database.models.operation_log_type import OperationLogType

from operations import operation_scheduler, operation_worker

from utils.database_utils import check_database_connection_from_url


MONITOR_CATEGORY_NAME = "Monitor"


class OperationHistoryModelView(ModelView):
    datamodel = SQLAInterface(OperationHistory)
    related_views = [OperationConfig, OperationHistory]

    list_columns = ['id', 'operation_config', 'start_date_time', 'end_date_time', 'is_successfully_ended', 'records_extracted', 'records_loaded']

    @action("view_operation_history_logs", "View Logs", confirmation=None, icon=None, multiple=False)
    def view_operation_history_logs(self, item):
        return redirect(f"/operationhistorylogmodelview/list/?_flt_0_operation_history={item.id}")

appbuilder.add_view(OperationHistoryModelView, "Operation History", category=MONITOR_CATEGORY_NAME)


class OperationHistoryLogModelView(ModelView):
    datamodel = SQLAInterface(OperationHistoryLog)
    related_views = [OperationHistoryLog, OperationLogType]

    list_columns = ['operation_history', 'operation_log_type', 'log_message', 'log_date_time']

appbuilder.add_view(OperationHistoryLogModelView, "Operation Logs", category=MONITOR_CATEGORY_NAME)


class ExtractFileModelView(ModelView):
    datamodel = SQLAInterface(ExtractFile)
    related_views = [ExtractFile, OperationHistory]

    list_columns = ['operation_history', 'source_name', 'extension', 'process_again']

    @action("extract_again", "Process Again", "Are you sure?", None, multiple=True, single=True)
    def extract_again(self, items):
        if isinstance(items, list):
            for item in items:
                item.process_again = True
        else:
            items.process_again = True
        db.session.commit()
        flash("Selected file(s) will be processed in the next operation run.", "success")
        return redirect("/extractfilemodelview/list/")

appbuilder.add_view(ExtractFileModelView, "Processed Files", category=MONITOR_CATEGORY_NAME)


class SystemView(BaseView):

    default_view = 'status'

    @expose('/status/')
    @has_access
    def status(self):
        """/systemview/status view shows user the health of the components of Open ETL."""
        app_db_health = check_database_connection_from_url(SQLALCHEMY_DATABASE_URI) == None
        staging_db_health = check_database_connection_from_url(STAGING_DATABASE_URI) == None
        worker_health = sum(map(lambda x: x.is_alive(), operation_worker.worker_threads)) == len(operation_worker.worker_threads)
        scheduler_health = operation_scheduler.operation_scheduler_thread.is_alive()
        self.update_redirect()
        return render_template("system_status.html", 
            appbuilder=self.appbuilder, 
            app_db_health=app_db_health,
            staging_db_health=staging_db_health,
            worker_health=worker_health,
            scheduler_health=scheduler_health)

appbuilder.add_view_no_menu(SystemView, "Status")
appbuilder.add_link("System Status", href='/systemview/status', category=MONITOR_CATEGORY_NAME)

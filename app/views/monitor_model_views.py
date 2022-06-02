from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from app import appbuilder

from app.models.operation_history import OperationHistory
from app.models.operation_config import OperationConfig
from app.models.operation_history_log import OperationHistoryLog
from app.models.operation_log_type import OperationLogType


MONITOR_CATEGORY_NAME = "Monitor"


class OperationHistoryModelView(ModelView):
    datamodel = SQLAInterface(OperationHistory)
    related_views = [OperationConfig, OperationHistory]

    list_columns = ['id', 'operation_config', 'start_date_time', 'end_date_time', 'is_successfully_ended', 'records_extracted', 'records_loaded']


appbuilder.add_view(OperationHistoryModelView, "Operation History", category=MONITOR_CATEGORY_NAME)


class OperationHistoryLogModelView(ModelView):
    datamodel = SQLAInterface(OperationHistoryLog)
    related_views = [OperationHistoryLog, OperationLogType]

    list_columns = ['operation_history', 'operation_log_type', 'log_message', 'log_date_time']

appbuilder.add_view(OperationHistoryLogModelView, "Operation Logs", category=MONITOR_CATEGORY_NAME)

from app import db

from database.models.operation_config import OperationConfig
from database.models.operation_history import OperationHistory


def create_dashboard_info():
    
    operation_configs = OperationConfig.get_all_enabled(db)

    dashboard_info = []

    for o_c in operation_configs:
        status = None
        last = OperationHistory.get_last(db, o_c.id)
        if last:
            status = last.is_successfully_ended
        operation_name = o_c.operation_name
        last_success = OperationHistory.get_last_success(db, o_c.id).end_date_time
        last_failure = OperationHistory.get_last_failure(db, o_c.id).end_date_time
        obj = DashboardInfo(status, operation_name, last_success, last_failure)
        dashboard_info.append(obj)

    return dashboard_info


class DashboardInfo:

    def __init__(self, status, operation_name, last_success, last_failure) -> None:
        self.status = status
        self.operation_name = operation_name
        self.last_success = last_success
        self.last_failure = last_failure

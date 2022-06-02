from app.models.operation_history_log import OperationHistoryLog
from app.models.operation_log_type import OperationLogTypeEnum


class BaseLoader:


    def __init__(self, db, operation_history) -> None:
        """
            Parameters:
                db: SQLA db object.
                operation_history: OperationHistory object.
        """
        self.db = db
        self.operation_history = operation_history
        self.operation_config = operation_history.operation_config
        self.load_target = self.operation_config.load_target


    def load_data(self, data, column_map, load_columns):
        """Interface method definition for loader objects."""
        raise NotImplementedError


    def log_load_amount(self, num):
        """Logs the loaded data amount to the corresponding operation_history table."""
        OperationHistoryLog.create(self.db, self.operation_history.id, f"{num} rows loaded.", OperationLogTypeEnum.INFO.value)
        self.operation_history.records_loaded = num
        self.db.session.commit()

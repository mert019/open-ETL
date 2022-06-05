from datetime import datetime, timedelta
import threading
from time import sleep

from app.models.operation_config import OperationConfig
from app.models.operation_history import OperationHistory
from app.models.operation_history_log import OperationHistoryLog
from app.models.operation_log_type import OperationLogTypeEnum
from app.models.schedule_unit import ScheduleUnitEnum


class OperationScheduler:


    def __init__(self, queue):
        self.queue = queue


    def run(self, db):
        self.db = db
        OperationConfig.set_all_is_in_process_to_false(self.db)
        self.operation_scheduler_thread = threading.Thread(target=self.schedule_loop)
        self.operation_scheduler_thread.daemon = True
        self.operation_scheduler_thread.start()


    def schedule_loop(self):
        while True:
            sleep(15)
            self.schedule()


    def schedule(self):
        
        current_time = datetime.now()

        operations = OperationConfig.get_all_enabled(self.db)

        for oper in operations:

            if oper.is_in_process:
                continue

            schedule_unit = oper.schedule_unit.id
            schedule_interval = oper.schedule_interval

            remove_duration = None
            if schedule_unit == ScheduleUnitEnum.MINUTE.value:
                remove_duration = timedelta(minutes=schedule_interval)
            elif schedule_unit == ScheduleUnitEnum.HOUR.value:
                remove_duration = timedelta(hours=schedule_interval)
            elif schedule_unit == ScheduleUnitEnum.DAY.value:
                remove_duration = timedelta(days=schedule_interval)
            else:
                raise RuntimeError(f"Schedule unit for operation {repr(oper)} could not matched.")

            earliest_possible_date = current_time - remove_duration

            oper_history = self.db.session.query(OperationHistory).filter(
                (OperationHistory.operation_config_id == oper.id)
                & (OperationHistory.start_date_time > earliest_possible_date)
            ).first()

            if (oper_history is None):
                operation_history_id = self.add_operation_to_queue(oper)
                print(f"{threading.currentThread().ident} OPERATION_SCHEDULER: Operation {repr(oper)} added to queue. Opertion history id: {operation_history_id}")
    

    def add_operation_to_queue(self, operation_config):
        """
            Creates operation history and adds it to queue.
                Parameters:
                    operation_config: OperationConfig object.
                Returns:
                    operation_history_id: (int) operation_history_id.
        """
        oper_history = OperationHistory.create(self.db, operation_config.id)
        operation_config.is_in_process = True
        self.db.session.commit()
        self.queue.put(oper_history.id)
        OperationHistoryLog.create(self.db, oper_history.id, "Added to queue.", OperationLogTypeEnum.INFO.value)
        return oper_history.id
        
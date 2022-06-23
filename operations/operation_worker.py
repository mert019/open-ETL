from datetime import datetime
from flask_appbuilder import SQLA
import logging
import pandas as pd
from queue import Queue
from time import sleep
import threading
import traceback

from database.models.extract_column import ExtractColumn
from database.models.load_column import LoadColumn
from database.models.operation_history_log import OperationHistoryLog
from database.models.operation_history import OperationHistory
from database.models.operation_log_type import OperationLogTypeEnum

from operations.extractors.database_extractor import DatabaseExtractor
from operations.extractors.extractor_factory import extractor_factory
from operations.loaders.loader_factory import loader_factory

from operations.staging_handler import StagingHandler


class OperationWorker:

    def __init__(self, queue:Queue, running_operations:set):
        self.queue = queue
        self.running_operations = running_operations
        self.finished_operations = []
        self.worker_threads = []


    def run(self, db:SQLA, workers=1):
        self.db = db
        # Operation workers
        for _ in range(workers):
            w_thread = threading.Thread(target=self.work_loop)
            w_thread.daemon =True
            self.worker_threads.append(w_thread)
            w_thread.start()
        # Operation finisher
        w_f_thread = threading.Thread(target=self.finish_operation_loop)
        w_f_thread.daemon = True
        self.worker_threads.append(w_f_thread)
        w_f_thread.start()


    def work_loop(self):
        while True:
            try:
                sleep(5)
                self.work_handler()
            except:
                self.db.session.rollback()
                logging.exception(f"{threading.currentThread().ident} OPERATION_WORKER ERROR:")


    def work_handler(self):

        if self.queue.qsize() > 0:

            queue_item = self.queue.get()
            print(f"{threading.currentThread().ident} OPERATION_WORKER: Queue item is taken. {queue_item}")
            OperationHistoryLog.create(self.db, queue_item, "Taken from queue.", OperationLogTypeEnum.INFO.value)

            operation_history = self.db.session.query(OperationHistory).filter_by(id=queue_item).first()
            
            try:
                self.work(queue_item)
                operation_history.is_successfully_ended = True
                OperationHistoryLog.create(self.db, queue_item, "Operation completed successfully.", OperationLogTypeEnum.INFO.value)
                print(f"{threading.currentThread().ident} OPERATION_WORKER: Operation completed successfully. OperationHistory: {queue_item}")

            except Exception as ex:
                operation_history.is_successfully_ended = False
                OperationHistoryLog.create(self.db, queue_item, f"Operation failed. {str(ex)}", OperationLogTypeEnum.ERROR.value)
                print(f"{threading.currentThread().ident} OPERATION_WORKER: Operation failed. OperationHistory: {queue_item}")
                traceback.print_exc()

            finally:
                operation_history.end_date_time = datetime.now()
                operation_history.operation_config.is_in_process = False
                self.finished_operations.append(queue_item)
                self.db.session.commit()


        else:
            print(f"{threading.currentThread().ident} OPERATION_WORKER: Queue is empty.")


    def work(self, operation_history_id):

        # get config information.
        operation_history = self.db.session.query(OperationHistory).filter_by(id=operation_history_id).first()
        operation_config = operation_history.operation_config
        extract_source = operation_config.extract_source
        load_target = operation_config.load_target
        load_columns = self.db.session.query(LoadColumn).filter_by(load_target_id=load_target.id).all()

        # create extractor object.
        extractor = extractor_factory(extract_source, operation_history, self.db)

        # create loader object.
        loader = loader_factory(load_target, operation_history, self.db)

        # extract data.
        data = extractor.get_data()

        # Use staging database only if transform query exists.
        if type(data) == pd.DataFrame and data.shape[0] != 0 and operation_config.transform_query and len(operation_config.transform_query) > 0:
            staging_handler = StagingHandler()
            # load data to staging database.
            staging_handler.load(data, operation_config.operation_name)
            OperationHistoryLog.create(self.db, operation_history.id, "Data loaded to staging database.", OperationLogTypeEnum.INFO.value)
            # extract data from staging database.
            data = staging_handler.extract(operation_config.transform_query)
            OperationHistoryLog.create(self.db, operation_history.id, f"{data.shape[0]} rows extracted from staging database.", OperationLogTypeEnum.INFO.value)

        # load data
        type(data) == pd.DataFrame and data.shape[0] != 0 and loader.load_data(data, load_columns)


    def finish_operation_loop(self) -> None:
        while True:
            try:
                sleep(5)
                self.finish_operation()
            except:
                self.db.session.rollback()
                logging.exception(f"{threading.currentThread().ident} OPERATION_WORKER (finish_operation) ERROR:")


    def finish_operation(self) -> None:
        """
            When the operation finishes, operation_config.is_in_process flag should set to False.
            On database connection errors, this flag may stuck in False value. 
            To prevent that situation finish_operation function added.
        """
        successfully_setted = []
        for operation_history_id in self.finished_operations:
            operation_history = self.db.session.query(OperationHistory).filter(
                OperationHistory.id == operation_history_id).first()
            operation_history.operation_config.is_in_process = False
            self.db.session.commit()
            successfully_setted.append(operation_history_id)
            if operation_history_id in self.running_operations:
                self.running_operations.remove(operation_history_id)
        for i in successfully_setted:
            self.finished_operations.remove(i)

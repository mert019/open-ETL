from time import sleep
import threading
from datetime import datetime
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

    def __init__(self, queue):
        self.queue = queue
        self.worker_threads = []


    def run(self, db, workers=1):
        self.db = db
        for _ in range(workers):
            w_thread = threading.Thread(target=self.work_loop)
            w_thread.daemon =True
            self.worker_threads.append(w_thread)
            w_thread.start()


    def work_loop(self):

        while True:
            sleep(5)

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
        if operation_config.transform_query and len(operation_config.transform_query) > 0:
            staging_handler = StagingHandler()
            # load data to staging database.
            staging_handler.load(data, operation_config.operation_name)
            OperationHistoryLog.create(self.db, operation_history.id, "Data loaded to staging database.", OperationLogTypeEnum.INFO.value)
            # extract data from staging database.
            data = staging_handler.extract(operation_config.transform_query)
            OperationHistoryLog.create(self.db, operation_history.id, f"{data.shape[0]} rows extracted from staging database.", OperationLogTypeEnum.INFO.value)

        # load data
        loader.load_data(data, load_columns)

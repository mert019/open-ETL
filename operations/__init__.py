from operations.operation_scheduler import OperationScheduler
from operations.operation_worker import OperationWorker
from queue import Queue

queue = Queue()

operation_scheduler = OperationScheduler(queue)

operation_worker = OperationWorker(queue)

from operations.operation_scheduler import OperationScheduler
from operations.operation_worker import OperationWorker
from queue import Queue


queue = Queue()

running_operations = set()

operation_scheduler = OperationScheduler(queue, running_operations)

operation_worker = OperationWorker(queue, running_operations)

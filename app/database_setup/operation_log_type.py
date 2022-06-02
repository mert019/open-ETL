from app import db

from app.models.operation_log_type import OperationLogType 



# from INFO
info_log_exists = db.session.query(OperationLogType).filter_by(log_type = "INFO").first()
if not info_log_exists:
    info_log = OperationLogType(log_type = "INFO")
    db.session.add(info_log)
    db.session.commit()

# from WARNING
warning_log_exists = db.session.query(OperationLogType).filter_by(log_type = "WARNING").first()
if not warning_log_exists:
    warning_log = OperationLogType(log_type = "WARNING")
    db.session.add(warning_log)
    db.session.commit()

# from ERROR
error_log_exists = db.session.query(OperationLogType).filter_by(log_type = "ERROR").first()
if not error_log_exists:
    error_log = OperationLogType(log_type = "ERROR")
    db.session.add(error_log)
    db.session.commit()

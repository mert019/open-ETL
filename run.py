from app import db, app
from app import models
db.create_all()
from app import database_setup


from operations import operation_scheduler
from operations import operation_worker
operation_scheduler.run(db)
operation_worker.run(db, 3)


from app import app
app.run(host="0.0.0.0", port=8080, debug=False)
# app.run(host="0.0.0.0", port=8080, debug=True)

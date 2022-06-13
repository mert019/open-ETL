from app import app

# Init database
from database import db
from database import models
db.create_all()
from database import setup

# Init operations
from operations import operation_scheduler
from operations import operation_worker
operation_scheduler.run(db)
operation_worker.run(db, 1)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)

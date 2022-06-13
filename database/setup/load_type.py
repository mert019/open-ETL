from database import db

from database.models.load_type import LoadType


# to database
to_db_exists = db.session.query(LoadType).filter_by(load_type = "TO_DATABASE").first()
if not to_db_exists:
    to_db = LoadType(load_type = "TO_DATABASE")
    db.session.add(to_db)
    db.session.commit()

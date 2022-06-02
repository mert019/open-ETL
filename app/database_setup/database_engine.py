from app import db

from app.models.database_engine import DatabaseEngine



# postgresql
postgresql_exists = db.session.query(DatabaseEngine).filter_by(engine_name = "Postgresql").first()
if not postgresql_exists:
    postgresql = DatabaseEngine(engine_name = "Postgresql")
    db.session.add(postgresql)
    db.session.commit()

# mssqlserver
mssqlserver_exists = db.session.query(DatabaseEngine).filter_by(engine_name = "MSSQLServer").first()
if not mssqlserver_exists:
    mssqlserver = DatabaseEngine(engine_name = "MSSQLServer")
    db.session.add(mssqlserver)
    db.session.commit()

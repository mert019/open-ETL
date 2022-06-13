from database.models.database_engine import DatabaseEngineEnum
from database.models.database_load_config import DatabaseLoadConfig
from database.models.load_type import LoadTypeEnum

from operations.loaders.to_database.mssqlserver_loader import MSSQLServerLoader
from operations.loaders.to_database.postgresql_loader import PostgresqlLoader


def loader_factory(load_target, operation_history, db):
    """
        Returns a ILoader type class.
        load_target: LoadTarget
        db: SQLA
    """

    loader = None

    # TO_DATABASE
    if load_target.load_type_id == LoadTypeEnum.TO_DATABASE.value:
        database_load_config = db.session.query(DatabaseLoadConfig).filter_by(load_target_id=load_target.id).first()
        database_engine = database_load_config.database_engine

        if database_engine.id == DatabaseEngineEnum.MSSQLSERVER.value:
            loader = MSSQLServerLoader(database_load_config, operation_history, db)
        elif database_engine.id == DatabaseEngineEnum.POSTGRESQL.value:
            loader = PostgresqlLoader(database_load_config, operation_history, db)
        else:
            raise ValueError(f"Database engine for DatabaseLoadConfig {database_load_config.id} could not matched.")

    return loader

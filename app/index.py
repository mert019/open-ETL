from datetime import datetime
from flask_appbuilder import IndexView, expose, has_access
from sqlalchemy import desc

from database import db
from database.models.operation_config import OperationConfig
from database.models.operation_history import OperationHistory

from operations import running_operations


class AppIndexView(IndexView):

    index_template = 'index.html'

    @expose("/")
    @has_access
    def index(self):
        operation_summary = {} # key: operation_config, value: list of operation history.
        operation_configs = db.session.query(OperationConfig).filter_by(show_on_dashboard=True).all()
        for o_c in operation_configs:
            # get latest 5 item.
            o_h = db.session.query(OperationHistory).filter_by(operation_config_id=o_c.id).order_by(desc(OperationHistory.start_date_time)).limit(5).all()
            operation_summary[o_c] = o_h
        updated_at = datetime.now()
        return self.render_template(self.index_template, appbuilder=self.appbuilder, operation_summary=operation_summary, updated_at=updated_at, running_operations=running_operations)

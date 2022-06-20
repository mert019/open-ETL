from flask import flash, redirect

from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, BS3PasswordFieldWidget, Select2AJAXWidget

from wtforms import TextAreaField, PasswordField
from wtforms.validators import DataRequired

from app import appbuilder

from database.models.database_connection import DatabaseConnection
from database.models.database_engine import DatabaseEngine
from database.models.ftp_connection import FtpConnection
from database.models.ftp_type import FTPType

from utils.database_utils import check_database_connection
from utils.ftp_utils import check_ftp_connection


CONNECTION_CATEGORY_NAME = "Connections"


class DatabaseConnectionModelView(ModelView):
    datamodel = SQLAInterface(DatabaseConnection)
    related_views = [DatabaseConnection, DatabaseEngine]

    list_columns = ['conn_name', 'conn_db_hostname', 'conn_db_name', 'database_engine']

    @action("check_connection", "Check Connection", confirmation=None, icon="fa-signal", multiple=False)
    def check_connection(self, item):
        error_message = check_database_connection(item)
        if error_message:
            flash(f"ERROR: {error_message}", 'warning')
        else:
            flash("Connection successful.", 'success')
        return redirect(f"/databaseconnectionmodelview/show/{item.id}")

appbuilder.add_view(DatabaseConnectionModelView, "Manage Database Connections", category=CONNECTION_CATEGORY_NAME)


class FtpConnectionModelView(ModelView):
    datamodel = SQLAInterface(FtpConnection)
    related_views = [FtpConnection, FTPType]

    list_columns = ['conn_name', 'ftp_hostname', 'ftp_type']

    @action("check_connection", "Check Connection", confirmation=None, icon="fa-signal", multiple=False)
    def check_connection(self, item):
        error_message = check_ftp_connection(item)
        if error_message:
            flash(f"ERROR: {error_message}", 'warning')
        else:
            flash("Connection successful.", 'success')
        return redirect(f"/ftpconnectionmodelview/show/{item.id}")

appbuilder.add_view(FtpConnectionModelView, "Manage FTP Connections", category=CONNECTION_CATEGORY_NAME)


# # TODO
# 'conn_db_password': PasswordField(
#             validators=[DataRequired()],
#             widget=BS3PasswordFieldWidget()),


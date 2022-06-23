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

    show_columns = ['database_engine', 'conn_name', 'conn_db_hostname', 'conn_db_port', 'conn_db_username', 'conn_db_name']

    label_columns = {
        "conn_name": "Connection Name",
        "conn_db_hostname": "Hostname",
        "conn_db_port": "Port",
        "conn_db_username": "Username",
        "conn_db_password": "Password",
        "conn_db_name": "Database Name",
    }

    add_form_extra_fields = {
        'conn_db_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget(),
            label=label_columns["conn_db_password"]),
    }

    edit_form_extra_fields = {
        'conn_db_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget(),
            label=label_columns["conn_db_password"]),
    }

    @action("test_connection", "Test Connection", confirmation=None, icon="fa-signal", multiple=False)
    def test_connection(self, item):
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

    show_columns = ['ftp_type', 'conn_name', 'ftp_hostname', 'ftp_port', 'ftp_username']

    label_columns = {
        "conn_name": "Connection Name",
        "ftp_hostname": "Hostname",
        "ftp_port": "Port",
        "ftp_username": "Username",
        "ftp_password": "Password",
    }

    add_form_extra_fields = {
        'ftp_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget(),
            label=label_columns["ftp_password"]),
    }

    edit_form_extra_fields = {
        'ftp_password': PasswordField(
            validators=[DataRequired()],
            widget=BS3PasswordFieldWidget(),
            label=label_columns["ftp_password"]),
    }
    
    @action("test_connection", "Test Connection", confirmation=None, icon="fa-signal", multiple=False)
    def test_connection(self, item):
        error_message = check_ftp_connection(item)
        if error_message:
            flash(f"ERROR: {error_message}", 'warning')
        else:
            flash("Connection successful.", 'success')
        return redirect(f"/ftpconnectionmodelview/show/{item.id}")

appbuilder.add_view(FtpConnectionModelView, "Manage FTP Connections", category=CONNECTION_CATEGORY_NAME)

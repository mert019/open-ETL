import pandas as pd
from sqlalchemy import column

from app.models.database_engine import DatabaseEngineEnum

from operations.loaders.loader_base import BaseLoader


class DatabaseLoader(BaseLoader):


    def __init__(self, database_load_config, operation_history, db) -> None:
        """
            Parameters:
                database_load_config: DatabaseLoadConfig object.
                operation_history: OperationHistory object.
                db: SQLA database object.
        """
        super().__init__(db, operation_history)

        self.database_load_config = database_load_config
        self.table = database_load_config.table_name
        self.database_engine = database_load_config.database_engine
    
        # connection info
        self.hostname = database_load_config.conn_db_hostname
        self.port = database_load_config.conn_db_port
        self.username = database_load_config.conn_db_username
        self.password = database_load_config.conn_db_password
        self.database = database_load_config.conn_db_name

        # database load actions
        self.start_transaction = database_load_config.start_transaction
        self.delete_all_before_load = database_load_config.delete_all_before_load
        self.insert_record = database_load_config.insert_record
        self.update_record = database_load_config.update_record
        self.use_column_maps_only = database_load_config.use_column_maps_only

        # query templates. These should be initialized in sub classes.
        self._delete_query_template = None
        self._transaction_query_template = None
        self._update_query_template = None
        self._insert_query_template = None
        self._upsert_query_template = None


    # region: properties
    @property
    def delete_query_template(self):
        return self._delete_query_template
    @delete_query_template.setter
    def delete_query_template(self, value):
        self._delete_query_template = value

    @property
    def transaction_query_template(self):
        return self._transaction_query_template
    @transaction_query_template.setter
    def transaction_query_template(self, value):
        self._transaction_query_template = value

    @property
    def update_query_template(self):
        return self._update_query_template
    @update_query_template.setter
    def update_query_template(self, value):
        self._update_query_template = value

    @property
    def insert_query_template(self):
        return self._insert_query_template
    @insert_query_template.setter
    def insert_query_template(self, value):
        self._insert_query_template = value

    @property
    def upsert_query_template(self):
        return self._upsert_query_template
    @upsert_query_template.setter
    def upsert_query_template(self, value):
        self._upsert_query_template = value
    # endregion


    def get_query(self, row_count, column_names, makes_unique_column_names):
        """Returns query to be executed as string."""
        query = ""

        if self.delete_all_before_load:
            query += self.get_delete_all_query()

        for row_index in range(row_count):

            part = self.get_template()
            sql_where_statement = ""
            sql_set_statement = ""
            sql_column_names = ""
            sql_insert_values = ""

            if self.update_record:
                sql_where_statement = self.get_where_statement(makes_unique_column_names, row_index)
                sql_set_statement = self.get_set_statement(column_names, row_index)

            if self.insert_record:
                sql_column_names = self.get_column_names(column_names)
                sql_insert_values = self.get_insert_values(column_names, row_index)

            # replace parameters with values
            if len(sql_where_statement) > 0:
                part = part.replace("$WHERE_STATEMENT$", sql_where_statement)
            if len(sql_set_statement) > 0:
                part = part.replace("$SET_STATEMENT$", sql_set_statement)
            if len(sql_column_names) > 0:
                part = part.replace("$COLUMN_NAMES$", sql_column_names)
            if len(sql_insert_values) > 0:
                part = part.replace("$INSERT_VALUES$", sql_insert_values)
            
            query += part
        
        query = query.replace("$TABLE_NAME$", self.table)
        query = self.get_transaction_query(query)

        return query


    def get_parameter_dict(self, df):
        """
            Returns parameter dictionary to use in query execution.
            Parameters:
                df: pandas.DataFrame
            Note: The data type converison that query execution does not support should be handled in here.
        """
        parameters = {}

        column_names = df.columns
        row_num = df.shape[0]
        
        df_dict = df.to_dict()

        # iterate rows
        for i in range(row_num):
            for col_name in column_names:

                val = df_dict[col_name][i]
                val_type = type(val)

                # type conversion
                if val_type == pd._libs.tslibs.timestamps.Timestamp:
                    val = val.to_pydatetime()

                parameters[f"val_{col_name}_{i}"] = val

        return parameters


    def get_transaction_query(self, query) -> str:

        """
            Adds transaction scripts to given query. Returns sql script as str.
            Parameteres: 
                query: str. Sql query to add transaction.
        """
        return self.transaction_query_template.replace("$QUERY$", query)


    def get_delete_all_query(self) -> str:
        """Returns sql script for deleting all rows."""
        return self.delete_query_template.replace("$TABLE_NAME$", self.table)


    def get_where_statement(self, makes_unique_column_names, row_index):
        """
            $WHERE_STATEMENT$
            Returns sql where statements for given column names and row index.
            Parameters:
                makes_unique_column_names: str list. Column names to be used in where statement.
                row_index: int. where statement row index to be written for row.
        """
        where_statement = ""
        for col_index in range(len(makes_unique_column_names)):
            if col_index > 0:
                where_statement += "AND "
            c_name = makes_unique_column_names[col_index]
            where_statement += f"{makes_unique_column_names[col_index]} = %(val_{c_name}_{row_index})s "
        return where_statement


    def get_set_statement(self, column_names, row_index):
        """
            $SET_STATEMENT$
            Returns sql where statements for given column names and row index.
            Parameters:
                column_names: str list. Column names to be used in set statement.
                row_index: int. set statement row index to be written for row.
        """
        set_statement = ""
        for col_index in range(len(column_names)):
            if col_index > 0:
                set_statement += ", "
            c_name = column_names[col_index]
            set_statement += f"{column_names[col_index]} = %(val_{c_name}_{row_index})s "
        return set_statement


    def get_column_names(self, column_names_list):
        """
            $COLUMN_NAMES$
            Returns sql column names to use in insert statement.
            Parameters:
                column_names: str list. Column names to be used in insert statement.
        """
        column_names = ""
        for col_index in range(len(column_names_list)):
            if col_index > 0:
                column_names += ", "
            column_names += f" {column_names_list[col_index]} "
        return column_names


    def get_insert_values(self, column_names, row_index):
        """
            $INSERT_VALUES$
            Returns sql insert values to use in insert statement.
            Parameters:
                column_names: str list. Column names to be used in insert statement.
                row_index: int. insert statement row index to be written for row.
        """
        insert_statement = ""
        for col_index in range(len(column_names)):
            if col_index > 0:
                insert_statement += ", "
            c_name = column_names[col_index]
            insert_statement += f"%(val_{c_name}_{row_index})s "
        return insert_statement


    def get_template(self) -> str:
        """Returns templates to be used in query generation."""
        template = None
        if self.update_record and not self.insert_record:
            template = self.update_query_template
        elif self.update_record and self.insert_record:
            template = self.upsert_query_template
        elif not self.update_record and self.insert_record:
            template = self.insert_query_template 
        return template

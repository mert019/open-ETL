import psycopg2

from operations.loaders.to_database.database_loader import DatabaseLoader


class PostgresqlLoader(DatabaseLoader):


    def __init__(self, database_load_config, operation_history, db) -> None:
        super().__init__(database_load_config, operation_history, db)

        delete_query_template = 'DELETE FROM "$TABLE_NAME$"; '

        transaction_query_template = f"""
                DO $$ BEGIN
                    $QUERY$
                END; $$;
            """

        update_query_template = """
                IF EXISTS(SELECT 1 FROM $TABLE_NAME$ WHERE $WHERE_STATEMENT$) THEN
                    UPDATE $TABLE_NAME$
                    SET $SET_STATEMENT$
                    WHERE $WHERE_STATEMENT$;
                END IF;
            """

        insert_query_template = """INSERT INTO $TABLE_NAME$ ( $COLUMN_NAMES$ ) VALUES ( $INSERT_VALUES$ );"""

        upsert_query_template = """
                IF EXISTS(SELECT 1 FROM $TABLE_NAME$ WHERE $WHERE_STATEMENT$) THEN
                    UPDATE $TABLE_NAME$
                    SET $SET_STATEMENT$
                    WHERE $WHERE_STATEMENT$;
                ELSE
                    INSERT INTO $TABLE_NAME$ ( $COLUMN_NAMES$ ) VALUES( $INSERT_VALUES$ );
                END IF;
            """
                
        self.delete_query_template = delete_query_template
        self.transaction_query_template = transaction_query_template
        self.update_query_template = update_query_template
        self.insert_query_template = insert_query_template
        self.upsert_query_template = upsert_query_template


    def load_data(self, df, column_map, load_columns):

        if not self.update_record and not self.insert_record:
            raise ValueError("update_record and insert_record cannot be false at the same time.")

        # TODO: Handle sql injection for table name and column names.

        # get unique column names
        makes_unique_column_names = []
        for obj in load_columns:
            if obj.is_makes_record_unique:
                makes_unique_column_names.append(obj.column_name)

        # if use only mapped columns selected, drop unmapped columns.
        if self.use_column_maps_only:
            mapped_load_column_names = []
            for obj in column_map:
                l_col = obj.load_column
                mapped_load_column_names.append(l_col.column_name)
            df.drop(df.columns.difference(mapped_load_column_names), axis=1, inplace=True)
            for c_name in makes_unique_column_names:
                if c_name not in mapped_load_column_names:
                    makes_unique_column_names.remove(c_name)

        if len(makes_unique_column_names) == 0 and self.update_record:
            raise ValueError("""Makes unique columns are not sepcified for update operation. 
                Or only use column maps option is causing to drop unmatched unique column names.""")

        # create load operation query and parameters.
        row_count = df.shape[0]
        query = self.get_query(row_count, df.columns, makes_unique_column_names)
        param_dict = self.get_parameter_dict(df)


        print(f"\n\n\nGENERATED QUERY FOR LOAD:\n\n{query}")
        print(f"\n\n\nPARAM DICT:\n\n{param_dict}\n\n\n")

        # database connection
        conn = psycopg2.connect(
            host=self.hostname,
            port=self.port,
            user=self.username,
            password=self.password,
            database=self.database)
        cur = conn.cursor()

        # execute query
        cur.execute(query, param_dict)
        conn.commit()

        self.log_load_amount(df.shape[0])

        # close database connection
        cur.close()
        conn.close()

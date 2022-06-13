from database.models.extract_column import ExtractColumn
from database.models.operation_history_log import OperationHistoryLog
from database.models.operation_log_type import OperationLogTypeEnum


class BaseExtractor:


    def __init__(self, db, operation_history) -> None:
        """
            Parameters:
                db: SQLA db object.
                operation_history: OperationHistory object.
        """
        self.db = db
        self.operation_history = operation_history
        self.operation_config = operation_history.operation_config
        self.extract_source = self.operation_config.extract_source


    def get_data(self):
        """Interface method definition for extractor objects."""
        raise NotImplementedError


    def log_extract_amount(self, num):
        """Logs the extacted data amount to the corresponding operation_history table."""
        OperationHistoryLog.create(self.db, self.operation_history.id, f"{num} rows extracted.", OperationLogTypeEnum.INFO.value)
        self.operation_history.records_extracted = num
        self.db.session.commit()


    def rename_data_table_columns(self, is_header_exists, df):
        """
            Gets the extract column info from database.
            If header exists, compares the column names with extract column if column index is specified.
                if extract_column.column_index does not match with the data table's column name in specified column index, throws exception.
            If header does not exist, sets column names. Throws exception if column index is greater than or equal to column amount.
            Parameters:
                is_header_exists: bool. Indicates if data table have headers.
                df: pd.DataFrame. Data table.
        """
        extract_columns = self.db.session.query(ExtractColumn).filter_by(extract_source_id=self.extract_source.id).all()

        df_columns = df.columns

        if is_header_exists:
            for e_c in extract_columns:
                col_index = e_c.column_index
                col_name = e_c.column_name
                if col_index and df_columns[col_index] != col_name:
                    raise ValueError(f"Based on ExtractColumn info, Column index {col_index} expected to be column name {col_name}. Instead got column name {df_columns[col_index]}.")

        else:
            col_index_name = {}
            for e_c in extract_columns:
                col_index = e_c.column_index
                col_name = e_c.column_name
                if col_index:
                    col_index_name[col_index] = col_name
            df.rename(columns=col_index_name, inplace=True)
        
        return df

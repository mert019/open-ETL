import pandas as pd

from database.models.extract_file import ExtractFile

from operations.extractors.from_ftp.ftp_extractor import FTPExtractor, DOWNLOAD_PATH


class CSVExtractor(FTPExtractor):


    def __init__(self, ftp_sourced_extract_config, operation_history, db) -> None:
        super().__init__(ftp_sourced_extract_config, operation_history, db)

        self.table_start_index = ftp_sourced_extract_config.table_start_index
        self.ignore_last_n_rows = ftp_sourced_extract_config.ignore_last_n_rows
        self.has_headers = ftp_sourced_extract_config.has_headers
        self.seperator = ftp_sourced_extract_config.seperator


    def get_data(self):
        """
            Downloads and reads csv files.
            Combines extracted data into a single pd.DataFrame.
            Returns pd.DataFrame.
        """
        self.download_files()

        extract_files = self.db.session.query(ExtractFile).filter_by(operation_history_id=self.operation_history.id).all()

        combined_data_frames = None

        # iterate files
        for extract_file in extract_files:

            header = None
            if self.has_headers:
                header = 0

            if self.table_start_index:
                header = self.table_start_index

            # read file
            path = DOWNLOAD_PATH + extract_file.unique_name
            df = pd.read_csv(path, header=header, sep=self.seperator)

            if self.ignore_last_n_rows:
                df.drop(df.tail(self.ignore_last_n_rows).index, inplace=True)
            
            # combine data table
            if combined_data_frames is None:
                combined_data_frames = df.copy()
            else:
                combined_data_frames = combined_data_frames.append(df, ignore_index=True)
        
        if combined_data_frames is not None:
            self.log_extract_amount(combined_data_frames.shape[0])
            combined_data_frames = self.rename_data_table_columns(self.has_headers, combined_data_frames)

        return combined_data_frames

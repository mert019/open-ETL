from ftplib import FTP
import paramiko
import re
from uuid import uuid4

from database.models.extract_file import ExtractFile
from database.models.extract_type import ExtractTypeEnum
from database.models.ftp_type import FTPTypeEnum
from database.models.operation_history import OperationHistory

from operations.extractors.extractor_base import BaseExtractor


DOWNLOAD_PATH = 'temp\\extract_files\\'


class FTPExtractor(BaseExtractor):


    def __init__(self, ftp_sourced_extract_config, operation_history, db) -> None:
        """
            Parameters:
                ftp_sourced_extract_config: CSVExtractConfig or ExcelExtractConfig object.
                operation_history: OperationHistory object.
                db: SQLA database object.
        """
        super().__init__(db, operation_history)

        self.ftp_sourced_extract_config = ftp_sourced_extract_config
        self.extract_directory = ftp_sourced_extract_config.extract_directory
        self.read_file_name = ftp_sourced_extract_config.read_file_name
        self.read_file_name_regex = ftp_sourced_extract_config.read_file_name_regex

        # connection info
        self.ftp_type = ftp_sourced_extract_config.ftp_type
        self.hostname = ftp_sourced_extract_config.ftp_hostname
        self.port = ftp_sourced_extract_config.ftp_port
        self.username = ftp_sourced_extract_config.ftp_username
        self.password = ftp_sourced_extract_config.ftp_password
    

    def get_operation_file_extension(self):
        """
            Returns file extension to be extracted. '.xlsx' or '.csv'.
            Throws exception if extract type could not matched.
        """
        file_extension = None
        if self.extract_source.extract_type_id == ExtractTypeEnum.FROM_CSV.value:
            file_extension = '.csv'
        elif self.extract_source.extract_type_id == ExtractTypeEnum.FROM_EXCEL.value:
            file_extension = '.xlsx' 
        else:
            raise ValueError(f"Extract type could not matched.")
        return file_extension


    def filter_files(self, file_list, already_extracted_files, extract_again_files, file_extension):
        """
            Filters file names based on the source config conditions.
            Returns matching files names to download as list of string.
            Parameters:
                file_list: list. All file names in the ftp directory as str.
                already_extracted_files: ExtractFile. Files to do not process again.
                extract_again_files: ExtractFile. Files to process again.
                file_extension: str.
        """
        #extension filter
        file_list = list(filter(lambda x: x.endswith(file_extension), file_list))

        #regex filter
        if self.read_file_name_regex and len(self.read_file_name_regex) > 0:
            file_list = list(filter(lambda x: bool(re.match(self.read_file_name_regex, x)), file_list))

        #name filter
        if self.read_file_name and len(self.read_file_name) > 0:
            file_list = list(filter(lambda x: self.read_file_name in x, file_list))

        #already extracted & extract again filter
        extract_again_file_names = []
        for eaf in extract_again_files:
            if eaf.source_name in file_list:
                extract_again_file_names.append(eaf.source_name)
        for a_e_f in already_extracted_files:
            if (a_e_f.source_name in file_list) and (a_e_f.source_name not in extract_again_file_names):
                file_list.remove(a_e_f.source_name)

        return file_list


    def ftp_download(self, already_extracted_files, extract_again_files):
        """
        Downloads the matching files names using ftp protocol.
        Parameters:
            already_extracted_files: ExtractFile. Files to do not process again.
            extract_again_files: ExtractFile. Files to process again.
        """
        # file extension
        file_extension = self.get_operation_file_extension()

        # connection
        ftp_server = FTP()
        ftp_server.connect(self.hostname, self.port)
        ftp_server.login(self.username, self.password)

        # change directory
        if self.extract_directory and self.extract_directory != ftp_server.pwd():
            ftp_server.cwd(self.extract_directory)

        # file names
        ftp_file_names = ftp_server.nlst()
        file_list = self.filter_files(ftp_file_names, already_extracted_files, extract_again_files, file_extension)

        #download files
        for file_name in file_list:
            unique_name = str(uuid4()) + file_extension
            filename = (file_name, DOWNLOAD_PATH + unique_name)
            with open(filename[1], "wb") as file:
                ftp_server.retrbinary(f"RETR {filename[0]}", file.write)
                ExtractFile.create(self.db, file_name, unique_name, file_extension, self.operation_history.id)
    
        # change extract again status
        for obj in extract_again_files:
            if obj.source_name in file_name:
                obj.process_again = False
                self.db.session.commit()


    def sftp_download(self, already_extracted_files, extract_again_files):
        """
            Downloads the matching files names using sftp protocol.
            Parameters:
                already_extracted_files: ExtractFile. Files to do not process again.
                extract_again_files: ExtractFile. Files to process again.
        """
        # file extension
        file_extension = self.get_operation_file_extension()

        # connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.hostname, self.port, self.username, self.password)
        sftp = ssh.open_sftp()
        sftp.chdir('.')

        # change directory
        if self.extract_directory and self.extract_directory != sftp.getcwd():
            sftp.chdir(self.extract_directory)

        # file names
        sftp_file_names = sftp.listdir()
        file_list = self.filter_files(sftp_file_names, already_extracted_files, extract_again_files, file_extension)

        # download files
        for file_name in file_list:
            unique_name = str(uuid4()) + file_extension
            filename = (file_name, DOWNLOAD_PATH + unique_name)
            sftp.get(filename[0], filename[1])
            ExtractFile.create(self.db, file_name, unique_name, file_extension, self.operation_history.id)


    def download_files(self):
        """
            Downloads files from ftp/sftp to extract data.
        """
        extract_again_files = self.db.session.query(ExtractFile).join(OperationHistory).filter(
            (OperationHistory.operation_config_id == self.operation_history.operation_config_id)
            & (ExtractFile.process_again == True)
            ).all()

        extract_again_file_names = []
        for obj in extract_again_files:
            extract_again_file_names.append(obj.source_name)

        already_extracted_files = self.db.session.query(ExtractFile).join(OperationHistory).filter(
            (OperationHistory.operation_config_id == self.operation_history.operation_config_id)
            & (ExtractFile.process_again == False)
            & (ExtractFile.source_name.notin_(extract_again_file_names))
            ).all()

        # download
        if self.ftp_type.id == FTPTypeEnum.FTP.value:
            self.ftp_download(already_extracted_files, extract_again_files)
        elif self.ftp_type.id == FTPTypeEnum.SFTP.value:
            self.sftp_download(already_extracted_files, extract_again_files)
        else:
            raise ValueError(f"FTP Type could not matched.")

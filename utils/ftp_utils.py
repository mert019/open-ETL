from ftplib import FTP
import paramiko

from database.models.ftp_type import FTPTypeEnum
from database.models.ftp_connection import FtpConnection


def check_ftp_connection(ftp_conn:FtpConnection):
    """
        Checks ftp/sftp connection success using the given ftp connection.
            Parameters:
                ftp_conn:
                    FtpConnection object.
            Returns:
                error_message: Returns error message if connection fails, otherwise returns None.
    """
    hostname = ftp_conn.ftp_hostname
    port = ftp_conn.ftp_port
    username = ftp_conn.ftp_username
    password = ftp_conn.ftp_password
    ftp_type_id = ftp_conn.ftp_type_id

    try:

        if ftp_type_id == FTPTypeEnum.FTP.value:
            ftp_server = FTP()
            ftp_server.connect(hostname, port)
            ftp_server.login(username, password)
            ftp_server.close()
            
        elif ftp_type_id == FTPTypeEnum.SFTP.value:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname, port, username, password)
            ssh.close()
            
        else:
            raise Exception(f"FTP type could not matched for ftp type id {ftp_type_id}")

    except Exception as ex:
        return str(ex)

    return None

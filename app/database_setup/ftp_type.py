from app import db

from app.models.ftp_type import FTPType


# ftp
ftp_exists = db.session.query(FTPType).filter_by(type_name = "FTP").first()
if not ftp_exists:
    ftp = FTPType(type_name = "FTP")
    db.session.add(ftp)
    db.session.commit()

# sftp
sftp_exists = db.session.query(FTPType).filter_by(type_name = "SFTP").first()
if not sftp_exists:
    sftp = FTPType(type_name = "SFTP")
    db.session.add(sftp)
    db.session.commit()

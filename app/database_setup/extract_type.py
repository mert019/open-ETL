from app import db

from app.models.extract_type import ExtractType



# from database
from_db_exists = db.session.query(ExtractType).filter_by(extract_type = "FROM_DATABASE").first()
if not from_db_exists:
    from_db = ExtractType(extract_type = "FROM_DATABASE")
    db.session.add(from_db)
    db.session.commit()

# from excel
from_excel_exists = db.session.query(ExtractType).filter_by(extract_type = "FROM_EXCEL").first()
if not from_excel_exists:
    from_excel = ExtractType(extract_type = "FROM_EXCEL")
    db.session.add(from_excel)
    db.session.commit()

# from csv
from_csv_exists = db.session.query(ExtractType).filter_by(extract_type = "FROM_CSV").first()
if not from_csv_exists:
    csv = ExtractType(extract_type = "FROM_CSV")
    db.session.add(csv)
    db.session.commit()

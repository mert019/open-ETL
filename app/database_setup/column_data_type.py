from app import db

from app.models.column_data_type import ColumnDataType



# integer
integer_cdt_exists = db.session.query(ColumnDataType).filter_by(data_type = "INT").first()
if not integer_cdt_exists:
    integer_cdt = ColumnDataType(data_type = "INT")
    db.session.add(integer_cdt)
    db.session.commit()

# float
float_cdt_exists = db.session.query(ColumnDataType).filter_by(data_type = "FLOAT").first()
if not float_cdt_exists:
    float_cdt = ColumnDataType(data_type = "FLOAT")
    db.session.add(float_cdt)
    db.session.commit()

# string
string_cdt_exists = db.session.query(ColumnDataType).filter_by(data_type = "STR").first()
if not string_cdt_exists:
    string_cdt = ColumnDataType(data_type = "STR")
    db.session.add(string_cdt)
    db.session.commit()

# boolean
boolean_cdt_exists = db.session.query(ColumnDataType).filter_by(data_type = "BOOL").first()
if not boolean_cdt_exists:
    boolean_cdt = ColumnDataType(data_type = "BOOL")
    db.session.add(boolean_cdt)
    db.session.commit()

# datetime
datetime_cdt_exists = db.session.query(ColumnDataType).filter_by(data_type = "DATETIME").first()
if not datetime_cdt_exists:
    datetime_cdt = ColumnDataType(data_type = "DATETIME")
    db.session.add(datetime_cdt)
    db.session.commit()

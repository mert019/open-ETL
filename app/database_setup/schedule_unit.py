from app import db

from app.models.schedule_unit import ScheduleUnit


# from minute
minute_exists = db.session.query(ScheduleUnit).filter_by(unit_name = "MINUTE").first()
if not minute_exists:
    minute = ScheduleUnit(unit_name = "MINUTE")
    db.session.add(minute)
    db.session.commit()

# from hour
hour_exists = db.session.query(ScheduleUnit).filter_by(unit_name = "HOUR").first()
if not hour_exists:
    hour = ScheduleUnit(unit_name = "HOUR")
    db.session.add(hour)
    db.session.commit()

# from day
day_exists = db.session.query(ScheduleUnit).filter_by(unit_name = "DAY").first()
if not day_exists:
    day = ScheduleUnit(unit_name = "DAY")
    db.session.add(day)
    db.session.commit()
    
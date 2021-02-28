from datetime import datetime, timedelta

from app import db
from app.models import StudyRoom, Slot


def get_studyroom(id):
    studyroom = StudyRoom.query.filter_by(id=id).first()
    return studyroom


def update_StudyroomInformation(studyroom, name, city, address, nation, postal_code, seats, mail_contact,
                                phone_num, toilette, vending_machines, wi_fi, electrical_outlets, printer, others):
    setattr(studyroom, 'name', name)
    setattr(studyroom, 'city', city)
    setattr(studyroom, 'address', address)
    setattr(studyroom, 'nation', nation)
    setattr(studyroom, 'postal_code', postal_code)
    setattr(studyroom, 'seats', seats)
    setattr(studyroom, 'mail_contact', mail_contact)
    setattr(studyroom, 'phone_num', phone_num)
    setattr(studyroom, 'toilette', toilette)
    setattr(studyroom, 'vending_machines', vending_machines)
    setattr(studyroom, 'wi_fi', wi_fi)
    setattr(studyroom, 'electrical_outlets', electrical_outlets)
    setattr(studyroom, 'printer', printer)
    setattr(studyroom, 'others', others)


def allow_reservation(studyroom):
    if not studyroom.bookable:
        setattr(studyroom, 'bookable', True)
        weekdays = {0: studyroom.monday, 1: studyroom.tuesday, 2: studyroom.wednesday, 3: studyroom.thursday,
                    4: studyroom.friday, 5: studyroom.saturday, 6: studyroom.sunday}
        for days in range(1, 7):
            data = datetime.utcnow().date() + timedelta(days=days)
            if weekdays[data.weekday()]:
                db.session.add(Slot(date=data, morning=True, afternoon=False, studyroom_id=studyroom.id,
                                    available_seats=studyroom.seats))
                db.session.add(Slot(date=data, morning=False, afternoon=True, studyroom_id=studyroom.id,
                                    available_seats=studyroom.seats))
    else:
        setattr(studyroom, 'bookable', False)


def search_studyroom(city, postal_code, name):
    results = StudyRoom.query

    if len(city) is not 0:
        results = results.filter(StudyRoom.city == city)
    if len(postal_code) is not 0:
        results = results.filter(StudyRoom.postal_code == postal_code)
    if len(name) is not 0:
        results = results.filter(StudyRoom.name == name)
    return results.all()

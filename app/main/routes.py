from app.models import User, Owner, StudyRoom, Reservation
from app.main import main
from app import db
from datetime import datetime


@main.before_app_first_request()
def database_creation():
    db.create_all()
    user1 = User(username='lollo', name='Lorenzo', surname='Costa', email='costalorenzo@mail.com', dob=datetime(year=1998, month=5, day=21), city='Turin', password='test')
    db.session.add(user1)
    db.session.commit()


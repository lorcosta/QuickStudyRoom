from app.models import User, Owner, StudyRoom, Reservation
from app.main import main
from app import db


@main.before_app_request
def database_creation():
    user1 = User(username='lollo', name='Lorenzo', surname='Costa', email='costalorenzo@mail.com', dob=21/05/1998, city='Turin', password='test')
    db.session.add(user1)
    db.session.commit()
